# main.py
import json
import random
import os
import re
import sqlite3

from difflib import SequenceMatcher

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


def normalize_answer(s: str) -> str:
    if s is None:
        return ""
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9 ]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Global movie storage
MOVIES = []


class GTMApp(App):

    # ✔ FINAL clean version
    def load_movies_from_db(self):
        conn = sqlite3.connect("movies.db")
        c = conn.cursor()

        try:
            c.execute("SELECT answer, characters, hints, alternatives, level, time FROM movies")
        except Exception as e:
            print("DB ERROR:", e)
            conn.close()
            return []

        data = []
        for row in c.fetchall():
            answer, chars, hints, alts, level, time = row

            # multiple correct answers allowed
            answers = [a.strip() for a in answer.split(",")]

            alt_list = [a.strip() for a in alts.split(",")] if alts else []

            data.append({
                "answers": answers,
                "characters": chars.split(","),
                "hints": hints.split(","),
                "alternatives": alt_list,
                "level": level,
                "time": time
            })

        conn.close()
        return data

    def build(self):

        global MOVIES

        # Load DB
        MOVIES = self.load_movies_from_db()

        # create level map
        self.level_map = {}
        for m in MOVIES:
            lvl = m.get("level", 1)
            self.level_map.setdefault(lvl, []).append(m)

        self.root = Builder.load_file("gtm.kv")

        self.level = 1
        self.score = 0
        self.lives = 3
        self.current = None
        self.hint_index = 0
        self.timer_event = None
        self.time_left = 0
        self.questions_answered_in_level = 0
        self.questions_to_clear_level = 3
        self.highscore_file = "gtm_highscore.json"
        self.highscore = self.load_highscore()

        # Play music
        self.bg_music = SoundLoader.load("bg.mp3")
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.play()

        self.update_ui_labels()
        self.next_question()
        return self.root

    def load_highscore(self):
        try:
            if os.path.exists(self.highscore_file):
                with open(self.highscore_file, "r") as f:
                    return json.load(f).get("highscore", 0)
        except:
            pass
        return 0

    def save_highscore(self):
        try:
            with open(self.highscore_file, "w") as f:
                json.dump({"highscore": self.highscore}, f)
        except:
            pass

    def show_autocorrect_popup(self, correct_answer, yes_callback, no_callback):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        msg = Label(text=f"Did you mean: [b]{correct_answer}[/b]?", markup=True)
        layout.add_widget(msg)

        btns = BoxLayout(spacing=10, size_hint=(1, 0.35))
        yes = Button(text="Yes")
        no = Button(text="No")
        btns.add_widget(yes)
        btns.add_widget(no)
        layout.add_widget(btns)

        popup = Popup(title="Suggestion", content=layout,
                      size_hint=(0.8, 0.4), auto_dismiss=False)

        yes.bind(on_press=lambda x: (popup.dismiss(), yes_callback()))
        no.bind(on_press=lambda x: (popup.dismiss(), no_callback()))

        popup.open()

    def pick_question_for_level(self):
        pool = self.level_map.get(self.level, [])
        if not pool:
            return None
        if self.current and len(pool) > 1:
            pool = [q for q in pool if q is not self.current]
        return random.choice(pool)

    def load_question(self, q):
        self.current = q
        self.hint_index = 0

        self.root.ids.characters_label.text = "\n".join(q.get("characters", []))
        self.root.ids.answer_input.text = ""
        self.root.ids.feedback_label.text = ""

        self.time_left = int(q.get("time", 25))
        self.update_timer_label()

        if self.timer_event:
            self.timer_event.cancel()

        self.timer_event = Clock.schedule_interval(self._tick, 1)

        self.update_ui_labels()

    def next_question(self, *args):
        if self.lives <= 0:
            self.show_game_over()
            return

        q = self.pick_question_for_level()
        if q:
            self.load_question(q)

    def _tick(self, dt):
        self.time_left -= 1
        self.update_timer_label()

        if self.time_left <= 0:
            self.root.ids.feedback_label.text = "Time up! -1 life"
            self.lives -= 1
            self.update_ui_labels()
            Clock.schedule_once(lambda dt: self._advance_after_timeout(), 1)

    def _advance_after_timeout(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        self.questions_answered_in_level += 1
        self.try_level_up()
        self.next_question()

    def update_timer_label(self):
        self.root.ids.timer_label.text = f"Time: {self.time_left}s"

    def mark_wrong(self):
        self.root.ids.feedback_label.text = "Wrong! -1 life"
        self.lives -= 1

        self.update_ui_labels()

        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        if self.lives <= 0:
            Clock.schedule_once(lambda dt: self.show_game_over(), 0.6)
        else:
            self.questions_answered_in_level += 1
            Clock.schedule_once(lambda dt: self.try_level_up_and_next(), 0.8)

    def process_correct(self, points=None):
        if points is None:
            points = 10 + (self.level - 1) * 5 + max(0, int(self.time_left / 2))

        self.score += points
        self.root.ids.feedback_label.text = f"Correct! +{points}"

        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        self.questions_answered_in_level += 1
        self.update_ui_labels()

        if self.score > self.highscore:
            self.highscore = self.score
            self.save_highscore()

        Clock.schedule_once(lambda dt: self.try_level_up_and_next(), 0.8)

    def check_answer(self):
        if not self.current:
            return

        user_raw = self.root.ids.answer_input.text
        user = normalize_answer(user_raw)

        corrects = []

        # add all main answers
        for ans in self.current.get("answers", []):
            corrects.append(normalize_answer(ans))

        # add alternatives
        for alt in self.current.get("alternatives", []):
            corrects.append(normalize_answer(alt))

        if user in corrects:
            self.process_correct()
            return

        best = max((similarity(user, c), c) for c in corrects)
        best_score, best_match = best

        # Perfect or near-perfect match
        if best_score >= 0.80 and user != "":
            self.process_correct()
            return

        # Suggestion popup
        if 0.60 <= best_score < 0.80 and user != "":
            suggestion = self.current.get("answers", [""])[0]

            self.show_autocorrect_popup(
                suggestion,
                yes_callback=lambda: self._autocorrect_yes(suggestion),
                no_callback=lambda: self._autocorrect_no()
            )
            return

        self.mark_wrong()

    def _autocorrect_yes(self, suggestion):
        self.root.ids.answer_input.text = suggestion
        self.process_correct()

    def _autocorrect_no(self):
        self.mark_wrong()

    def try_level_up_and_next(self):
        self.try_level_up()
        self.next_question()

    def try_level_up(self):
        if self.questions_answered_in_level >= self.questions_to_clear_level:
            self.questions_answered_in_level = 0

            levels = sorted(self.level_map.keys())
            idx = levels.index(self.level)

            if idx + 1 < len(levels):
                self.level = levels[idx + 1]
                self.root.ids.feedback_label.text = f"Level Up! Now {self.level}"
            else:
                self.root.ids.feedback_label.text = "Stage Cleared!"

        self.update_ui_labels()

    def show_hint(self):
        if not self.current:
            return

        hints = self.current.get("hints", [])
        if self.hint_index < len(hints):
            hint = hints[self.hint_index]
            self.hint_index += 1

            self.score = max(0, self.score - 5)
            self.root.ids.feedback_label.text = f"Hint: {hint} (-5)"

            self.update_ui_labels()
        else:
            self.root.ids.feedback_label.text = "No more hints."

    def skip_question(self):
        self.lives -= 2

        if self.lives <= 0:
            self.show_game_over()
            return

        self.root.ids.feedback_label.text = "Skipped (-2)"

        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        self.questions_answered_in_level += 1
        self.try_level_up_and_next()

    def update_ui_labels(self):
        self.root.ids.level_label.text = f"Level: {self.level}"
        self.root.ids.score_label.text = f"Score: {self.score}"
        self.root.ids.lives_label.text = f"Lives: {self.lives}"
        self.root.ids.highscore_label.text = f"High: {self.highscore}"

    def show_game_over(self):
        if self.timer_event:
            self.timer_event.cancel()

        content = Label(text=f"Game Over!\nScore: {self.score}\nHigh: {self.highscore}")
        popup = Popup(title="Game Over", content=content, size_hint=(0.7, 0.4))
        popup.open()

        self.level = 1
        self.score = 0
        self.lives = 3
        self.questions_answered_in_level = 0
        self.update_ui_labels()

    def restart_game(self):
        self.level = 1
        self.score = 0
        self.lives = 3
        self.questions_answered_in_level = 0

        if self.timer_event:
            self.timer_event.cancel()

        self.update_ui_labels()
        self.next_question()


if __name__ == "__main__":
    GTMApp().run()
