# Voice Test

## What this does

This is the first runnable voice milestone for the project. It generates a real audio file for the clinic agent using OpenAI text-to-speech, so you can hear how the voice sounds before wiring in Twilio or full live call flows.

## File

- [run_voice_test.py](../scripts/run_voice_test.py)

## Quick start

1. Create a local `.env` file in the project root.
2. Add your API key:

```env
OPENAI_API_KEY=your_real_openai_api_key
```

3. Run a dry preview first:

```powershell
python .\scripts\run_voice_test.py --dry-run
```

4. Generate the audio:

```powershell
python .\scripts\run_voice_test.py --open
```

## Default behavior

By default, the script:

- uses the `reminder` scenario
- uses the `gpt-4o-mini-tts` model
- uses the `coral` voice
- saves output to `outputs/voice/reminder_voice_test.mp3`

## Useful examples

Generate a feedback call:

```powershell
python .\scripts\run_voice_test.py --scenario feedback --open
```

Generate a follow-up with custom patient details:

```powershell
python .\scripts\run_voice_test.py `
  --scenario followup `
  --patient-name "Maria" `
  --clinic-name "Northside Clinic" `
  --provider-name "Dr. Lee" `
  --open
```

Speak fully custom text:

```powershell
python .\scripts\run_voice_test.py `
  --text "Hello, this is your clinic calling to confirm your appointment for tomorrow at 2 PM." `
  --voice sage `
  --open
```

Generate a WAV file instead of MP3:

```powershell
python .\scripts\run_voice_test.py --response-format wav
```

## Next step after this

Once this local voice test sounds right, the next milestone is a Twilio outbound call test so the same voice flow can be heard over the phone.
