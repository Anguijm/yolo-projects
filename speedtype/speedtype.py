#!/usr/bin/env python3
"""speedtype - A typing speed test using real code snippets, right in your terminal."""

import argparse
import curses
import glob
import json
import os
import random
import time

HISTORY_FILE = os.path.expanduser("~/.speedtype_history.json")

# Built-in code samples as fallback
BUILTIN_SAMPLES = {
    "python": [
        '''\
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b''',
        '''\
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def is_empty(self):
        return len(self.items) == 0''',
        '''\
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result''',
        '''\
def read_csv(filename):
    rows = []
    with open(filename, "r") as f:
        headers = f.readline().strip().split(",")
        for line in f:
            values = line.strip().split(",")
            rows.append(dict(zip(headers, values)))
    return rows''',
        '''\
from collections import Counter

def word_frequency(text):
    words = text.lower().split()
    counts = Counter(words)
    for word, count in counts.most_common(10):
        print(f"{word}: {count}")''',
    ],
    "js": [
        '''\
function debounce(fn, delay) {
  let timer = null;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}''',
        '''\
class EventEmitter {
  constructor() {
    this.events = {};
  }
  on(event, listener) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(listener);
  }
  emit(event, ...args) {
    const listeners = this.events[event] || [];
    listeners.forEach(fn => fn(...args));
  }
}''',
        '''\
async function fetchJSON(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (err) {
    console.error("Fetch failed:", err.message);
    return null;
  }
}''',
        '''\
function flattenArray(arr) {
  const result = [];
  const stack = [...arr];
  while (stack.length) {
    const item = stack.pop();
    if (Array.isArray(item)) {
      stack.push(...item);
    } else {
      result.unshift(item);
    }
  }
  return result;
}''',
    ],
    "go": [
        '''\
func reverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}''',
        '''\
func worker(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		fmt.Printf("worker %d processing job %d\\n", id, j)
		time.Sleep(time.Second)
		results <- j * 2
	}
}

func main() {
	jobs := make(chan int, 5)
	results := make(chan int, 5)
	for w := 1; w <= 3; w++ {
		go worker(w, jobs, results)
	}
	for j := 1; j <= 5; j++ {
		jobs <- j
	}
	close(jobs)
	for a := 1; a <= 5; a++ {
		fmt.Println(<-results)
	}
}''',
        '''\
type Cache struct {
	mu    sync.RWMutex
	items map[string]string
}

func NewCache() *Cache {
	return &Cache{items: make(map[string]string)}
}

func (c *Cache) Get(key string) (string, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	val, ok := c.items[key]
	return val, ok
}

func (c *Cache) Set(key, value string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.items[key] = value
}''',
    ],
}

# File extensions for each language
LANG_EXTENSIONS = {
    "python": "*.py",
    "js": "*.js",
    "go": "*.go",
}

SCAN_DIRS = [
    os.path.expanduser("~/projects"),
    os.path.expanduser("~/src"),
    os.path.expanduser("~/code"),
    os.path.expanduser("~/yolo_projects"),
    os.path.expanduser("~/Documents"),
    "/tmp",
]

# Max lines for a snippet extracted from a real file
SNIPPET_MIN_LINES = 4
SNIPPET_MAX_LINES = 15
MAX_SNIPPET_WIDTH = 80


def scan_for_snippets(lang):
    """Try to find real code snippets on the machine."""
    ext = LANG_EXTENSIONS.get(lang)
    if not ext:
        return []

    found_files = []
    for scan_dir in SCAN_DIRS:
        if not os.path.isdir(scan_dir):
            continue
        pattern = os.path.join(scan_dir, "**", ext)
        try:
            files = glob.glob(pattern, recursive=True)
            # Skip hidden dirs, node_modules, venvs, etc.
            files = [
                f for f in files
                if not any(
                    part.startswith(".") or part in ("node_modules", "venv", "__pycache__", "site-packages")
                    for part in f.split(os.sep)
                )
            ]
            found_files.extend(files)
        except Exception:
            continue

    if not found_files:
        return []

    random.shuffle(found_files)
    snippets = []

    for filepath in found_files[:50]:  # don't scan too many
        try:
            with open(filepath, "r", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            continue

        if len(lines) < SNIPPET_MIN_LINES:
            continue

        # Pick a random chunk
        max_start = max(0, len(lines) - SNIPPET_MIN_LINES)
        start = random.randint(0, max_start)
        length = random.randint(SNIPPET_MIN_LINES, SNIPPET_MAX_LINES)
        chunk = lines[start : start + length]

        # Clean up: skip if lines are too long or contain weird chars
        text = "".join(chunk).rstrip()
        if not text or any(len(l) > MAX_SNIPPET_WIDTH for l in text.splitlines()):
            continue
        # Skip binary-looking content
        if "\x00" in text:
            continue

        snippets.append(text)
        if len(snippets) >= 10:
            break

    return snippets


def get_snippet(lang=None):
    """Get a random code snippet, preferring real files, falling back to builtins."""
    langs = [lang] if lang else list(BUILTIN_SAMPLES.keys())

    if lang:
        real = scan_for_snippets(lang)
        if real:
            return random.choice(real), lang

    chosen_lang = random.choice(langs)
    return random.choice(BUILTIN_SAMPLES[chosen_lang]), chosen_lang


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_result(result):
    history = load_history()
    history.append(result)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def show_history():
    history = load_history()
    if not history:
        print("No history yet. Run a typing test first!")
        return

    print(f"{'#':<4} {'Date':<20} {'Lang':<8} {'WPM':<8} {'Acc%':<8} {'Time':<8}")
    print("-" * 56)
    for i, entry in enumerate(history[-20:], 1):  # show last 20
        print(
            f"{i:<4} {entry.get('date', '?'):<20} {entry.get('lang', '?'):<8} "
            f"{entry.get('wpm', 0):<8.1f} {entry.get('accuracy', 0):<8.1f} "
            f"{entry.get('time', 0):<8.1f}"
        )
    print(f"\nTotal sessions: {len(history)}")
    if history:
        wpms = [e.get("wpm", 0) for e in history]
        print(f"Average WPM: {sum(wpms) / len(wpms):.1f}")
        print(f"Best WPM: {max(wpms):.1f}")


def run_typing_test(stdscr, snippet, lang):
    """Main curses-based typing test."""
    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)   # correct
    curses.init_pair(2, curses.COLOR_RED, -1)      # wrong
    curses.init_pair(3, curses.COLOR_YELLOW, -1)   # status
    curses.init_pair(4, curses.COLOR_CYAN, -1)     # header

    stdscr.clear()
    stdscr.nodelay(False)
    stdscr.timeout(-1)

    lines = snippet.splitlines()
    typed = []  # list of chars typed so far
    start_time = None
    total_chars = len(snippet)

    while True:
        stdscr.erase()
        max_y, max_x = stdscr.getmaxyx()

        # Header
        header = f" speedtype | lang: {lang} | {total_chars} chars "
        try:
            stdscr.addstr(0, 0, header, curses.color_pair(4) | curses.A_BOLD)
        except curses.error:
            pass

        # Calculate live stats
        typed_len = len(typed)
        if start_time and typed_len > 0:
            elapsed = time.time() - start_time
            if elapsed > 0:
                words = typed_len / 5.0
                wpm = (words / elapsed) * 60
            else:
                wpm = 0.0
            correct = sum(1 for i, c in enumerate(typed) if i < total_chars and c == snippet[i])
            accuracy = (correct / typed_len * 100) if typed_len > 0 else 100.0
        else:
            wpm = 0.0
            accuracy = 100.0
            elapsed = 0.0

        # Status line
        status = f" WPM: {wpm:.0f} | Accuracy: {accuracy:.0f}% | {typed_len}/{total_chars} chars "
        try:
            stdscr.addstr(1, 0, status, curses.color_pair(3))
        except curses.error:
            pass

        # Render snippet with coloring
        row = 3
        col = 0
        char_idx = 0
        for line in lines:
            if row >= max_y - 2:
                break
            col = 0
            for ch in line:
                if col >= max_x - 1:
                    break
                if char_idx < typed_len:
                    if typed[char_idx] == ch:
                        attr = curses.color_pair(1)  # green
                    else:
                        attr = curses.color_pair(2) | curses.A_UNDERLINE  # red
                elif char_idx == typed_len:
                    attr = curses.A_REVERSE  # cursor position
                else:
                    attr = curses.A_DIM
                try:
                    stdscr.addch(row, col, ch, attr)
                except curses.error:
                    pass
                char_idx += 1
                col += 1

            # Handle the newline character in snippet
            if char_idx < total_chars:
                # There's a \n in the snippet between lines
                if char_idx < typed_len:
                    pass  # already typed past this newline
                elif char_idx == typed_len:
                    # Show cursor at end of line
                    try:
                        stdscr.addch(row, col, " ", curses.A_REVERSE)
                    except curses.error:
                        pass
                char_idx += 1  # count the newline

            row += 1

        # Instructions at bottom
        try:
            stdscr.addstr(max_y - 1, 0, " ESC=quit | Just start typing...", curses.A_DIM)
        except curses.error:
            pass

        stdscr.refresh()

        # Check if done
        if typed_len >= total_chars:
            break

        # Get input
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            return None

        if key == 27:  # ESC
            return None

        if key in (curses.KEY_BACKSPACE, 127, 8):
            if typed:
                typed.pop()
            continue

        if key == curses.KEY_RESIZE:
            continue

        # Ignore other special keys
        if key < 0 or key > 255:
            continue

        ch = chr(key)

        # Start timer on first keypress
        if start_time is None:
            start_time = time.time()

        # Handle Enter as newline
        if ch == "\n" or ch == "\r":
            typed.append("\n")
        else:
            typed.append(ch)

    # Done!
    end_time = time.time()
    elapsed = end_time - start_time if start_time else 0
    correct = sum(1 for i, c in enumerate(typed) if i < total_chars and c == snippet[i])
    accuracy = (correct / total_chars * 100) if total_chars > 0 else 100.0
    words = total_chars / 5.0
    wpm = (words / elapsed) * 60 if elapsed > 0 else 0

    return {
        "wpm": round(wpm, 1),
        "accuracy": round(accuracy, 1),
        "time": round(elapsed, 1),
        "chars": total_chars,
        "correct": correct,
        "lang": lang,
    }


def show_results_screen(stdscr, result):
    """Show final results and wait for keypress."""
    stdscr.erase()
    curses.init_pair(5, curses.COLOR_WHITE, -1)

    lines = [
        "",
        "  === RESULTS ===",
        "",
        f"  WPM:        {result['wpm']}",
        f"  Accuracy:   {result['accuracy']}%",
        f"  Time:       {result['time']}s",
        f"  Characters: {result['correct']}/{result['chars']} correct",
        f"  Language:   {result['lang']}",
        "",
        "  Press any key to exit...",
    ]

    for i, line in enumerate(lines):
        try:
            stdscr.addstr(i, 0, line, curses.color_pair(5) | curses.A_BOLD)
        except curses.error:
            pass

    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()


def main_curses(stdscr, lang):
    snippet, chosen_lang = get_snippet(lang)
    result = run_typing_test(stdscr, snippet, chosen_lang)

    if result is None:
        return  # user quit

    # Add timestamp
    result["date"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # Save to history
    save_result(result)

    # Show results
    show_results_screen(stdscr, result)


def main():
    parser = argparse.ArgumentParser(
        description="speedtype - typing speed test with real code snippets"
    )
    parser.add_argument(
        "--history", action="store_true", help="Show past results"
    )
    parser.add_argument(
        "--lang",
        choices=["python", "js", "go"],
        default=None,
        help="Filter snippet language",
    )
    args = parser.parse_args()

    if args.history:
        show_history()
        return

    curses.wrapper(lambda stdscr: main_curses(stdscr, args.lang))


if __name__ == "__main__":
    main()
