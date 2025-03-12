.PHONY: portfolio

portfolio: main.py manim.cfg
	uv run manim -c manim.cfg main.py VWPAnimation --format=webm

dev: main.py
	while inotifywait -e close_write main.py; do uv run manim -c manim.cfg main.py VWPAnimation; done
