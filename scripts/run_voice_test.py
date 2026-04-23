import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = ROOT_DIR / "outputs" / "voice"
OPENAI_SPEECH_URL = "https://api.openai.com/v1/audio/speech"

DEFAULT_INSTRUCTIONS = (
    "Speak in a calm, warm, professional clinic receptionist tone. "
    "Use clear pronunciation, short pauses, and a reassuring delivery."
)

SCENARIOS = {
    "reminder": (
        "Hello {patient_name}, this is a reminder from {clinic_name}. "
        "You have an appointment on {appointment_date} at {appointment_time} "
        "with {provider_name}. Please say confirm to keep your appointment, "
        "or say reschedule if you need a different time."
    ),
    "followup": (
        "Hello {patient_name}, this is a follow-up call from {clinic_name}. "
        "We are checking in after your recent visit with {provider_name}. "
        "If you have an administrative question, would like a callback, "
        "or want to leave feedback, please let us know."
    ),
    "feedback": (
        "Hello {patient_name}, this is {clinic_name}. "
        "We are calling to ask about your recent experience. "
        "Please tell us if you were satisfied with your visit, "
        "or if you would like a staff member to follow up."
    ),
}


def load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def build_message(args: argparse.Namespace) -> str:
    if args.text:
        return args.text

    template = SCENARIOS[args.scenario]
    return template.format(
        patient_name=args.patient_name,
        clinic_name=args.clinic_name,
        appointment_date=args.appointment_date,
        appointment_time=args.appointment_time,
        provider_name=args.provider_name,
    )


def create_speech(
    *,
    api_key: str,
    text: str,
    voice: str,
    model: str,
    instructions: str,
    response_format: str,
    speed: float,
) -> bytes:
    payload = json.dumps(
        {
            "model": model,
            "voice": voice,
            "input": text,
            "instructions": instructions,
            "response_format": response_format,
            "speed": speed,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        OPENAI_SPEECH_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"OpenAI speech request failed with HTTP {exc.code}: {error_body}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach OpenAI speech API: {exc.reason}") from exc


def maybe_open_file(file_path: Path) -> None:
    if not file_path.exists():
        return

    if sys.platform.startswith("win"):
        os.startfile(str(file_path))  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        os.system(f'open "{file_path}"')
    else:
        os.system(f'xdg-open "{file_path}"')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a first runnable clinic-agent voice test as an audio file."
    )
    parser.add_argument(
        "--scenario",
        choices=sorted(SCENARIOS.keys()),
        default="reminder",
        help="Choose a preset clinic-agent scenario.",
    )
    parser.add_argument(
        "--text",
        help="Custom text to speak. If set, it overrides the preset scenario template.",
    )
    parser.add_argument("--patient-name", default="Jordan")
    parser.add_argument("--clinic-name", default="Sunrise Family Clinic")
    parser.add_argument("--appointment-date", default="April 29")
    parser.add_argument("--appointment-time", default="10:30 AM")
    parser.add_argument("--provider-name", default="Dr. Patel")
    parser.add_argument("--voice", default="coral")
    parser.add_argument("--model", default="gpt-4o-mini-tts")
    parser.add_argument("--response-format", default="mp3", choices=["mp3", "wav", "aac", "flac", "opus", "pcm"])
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--instructions", default=DEFAULT_INSTRUCTIONS)
    parser.add_argument(
        "--output",
        help="Optional output file path. Defaults to outputs/voice/<scenario>_voice_test.<format>",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the generated script and output path without calling the API.",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the generated audio file after it is saved.",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv(ROOT_DIR / ".env")
    args = parse_args()

    text = build_message(args)
    output_path = (
        Path(args.output)
        if args.output
        else DEFAULT_OUTPUT_DIR / f"{args.scenario}_voice_test.{args.response_format}"
    )
    transcript_path = output_path.with_suffix(".txt")

    print("Scenario:", args.scenario)
    print("Voice:", args.voice)
    print("Model:", args.model)
    print("Output:", output_path.resolve())
    print("\nMessage:\n")
    print(text)

    if args.dry_run:
        return 0

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key":
        print(
            "\nOPENAI_API_KEY is missing. Add it to your environment or to a local .env file in the project root.",
            file=sys.stderr,
        )
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    audio_bytes = create_speech(
        api_key=api_key,
        text=text,
        voice=args.voice,
        model=args.model,
        instructions=args.instructions,
        response_format=args.response_format,
        speed=args.speed,
    )

    output_path.write_bytes(audio_bytes)
    transcript_path.write_text(text, encoding="utf-8")

    print(f"\nSaved audio to: {output_path.resolve()}")
    print(f"Saved transcript to: {transcript_path.resolve()}")

    if args.open:
        maybe_open_file(output_path.resolve())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
