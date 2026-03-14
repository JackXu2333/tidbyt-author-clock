"""Patch missing quotes into author_clock.star"""
import re


def escape_starlark(s):
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    result = []
    for c in s:
        if ord(c) > 127:
            result.append("\\u%04x" % ord(c))
        else:
            result.append(c)
    return "".join(result)


def make_entry(b, t, a, au):
    return (
        f'        {{"b": "{escape_starlark(b)}", "t": "{escape_starlark(t)}",'
        f' "a": "{escape_starlark(a)}", "au": "{escape_starlark(au)}"}}'
    )


NEW_ENTRIES = {
    # From CSV (nsfw-labeled but clean text)
    "01_28": [{"b": "ed at the police station. I di", "t": "1.28 a.m.", "a": " but I knew he was there becau", "au": "Mark Haddon"}],
    "02_51": [{"b": "Thursday ", "t": "2:51 A.M.", "a": "A very wet, very annoyed Micha", "au": "Thomas Hoover"}],
    "04_26": [{"b": "At ", "t": "twenty-six minutes past four", "a": ", she was pronounced dead.", "au": "Ann Rule"}],
    "04_28": [{"b": "and was disheartened to discov", "t": "0428", "a": " hours.", "au": "Glenn Smith"}],
    "04_44": [{"b": "At ", "t": "0444 hours", "a": " yesterday morning, the landing craft was taken.", "au": "Robert J. Sawyer"}],
    "05_31": [{"b": "", "t": "5:31", "a": " - on the phone: 'We gotta go in there and get those ballots!'", "au": "Hunter S Thompson"}],
    "05_47": [{"b": "Before dawn. It was ", "t": "forty-seven minutes past five", "a": ". On a Sunday.", "au": "Cassie Miles"}],
    "07_22": [{"b": "", "t": "7:22 A.M.", "a": "Do you know how to handle this?", "au": "Thomas Hoover"}],
    "11_22": [{"b": "appeared here yesterday at approximately ", "t": "11:22 a.m.", "a": ", wanting to know if anybody had seen his dog.", "au": "Craig Johnson"}],
    "12_34": [{"b": "", "t": "12:34 P.M.", "a": "W.B., we've got a problem, he said into the microphone.", "au": "Thomas Hoover"}],
    "13_04": [{"b": "It's ", "t": "four minutes past one", "a": "! He frantically seized hold of the steps.", "au": "Robert Tressell"}],
    "13_37": [{"b": "he was on the job, and he scribbled ", "t": "1.37 pm", "a": ". Subject appears to be getting nervous.", "au": "William Monahan"}],
    "13_56": [{"b": "", "t": "1:56 P.M.", "a": "Katelyn was out of the dorm room, off doing whatever she did.", "au": "J. Ryan Stradal"}],
    "17_34": [{"b": "At five-thirty. I arrived about ", "t": "four minutes later", "a": ". Judging by the appearance of the blood.", "au": "P.D. James"}],
    "17_41": [{"b": "All right, people. Sunset's at ", "t": "17:41", "a": " and we've got twenty-three kilometres to go.", "au": "Tanya Huff"}],
    "19_44": [{"b": "", "t": "7:44 P.M.", "a": "Vance watched as the helicopter approached the destroyer.", "au": "Thomas Hoover"}],
    "21_44": [{"b": "The island fell at ", "t": "sixteen minutes to ten o'clock", "a": " that January night in 1671.", "au": "Charles Stough"}],
    "23_26": [{"b": "Los Angeles. ", "t": "11:26 p.m.", "a": " In a dark red room, a tall woman dressed in black.", "au": "Neil Gaiman"}],
    # Manual entries for absent / truly-crude times
    "01_41": [{"b": "He checked the time: ", "t": "one forty-one in the morning", "a": ". The city had finally gone quiet.", "au": "Anonymous"}],
    "01_46": [{"b": "It was ", "t": "one forty-six", "a": ". She lay still, listening to the rain.", "au": "Anonymous"}],
    "06_06": [{"b": "The hall clock struck ", "t": "six minutes past six", "a": ", and the house stirred slowly to life.", "au": "Anonymous"}],
    "06_07": [{"b": "At ", "t": "seven minutes past six", "a": ", the light had barely changed, but she was already dressed.", "au": "Anonymous"}],
    "06_18": [{"b": "", "t": "Six eighteen", "a": ". Too early for most of the world, but not for him.", "au": "Anonymous"}],
    "08_21": [{"b": "It was ", "t": "twenty-one minutes past eight", "a": " when he first saw her standing at the corner.", "au": "Anonymous"}],
    "08_46": [{"b": "The clock above the fireplace read ", "t": "eight forty-six", "a": ", and no one had yet spoken.", "au": "Anonymous"}],
    "10_28": [{"b": "By ", "t": "ten twenty-eight", "a": " the meeting had already gone badly wrong.", "au": "Anonymous"}],
    "11_46": [{"b": "At ", "t": "eleven forty-six", "a": " she turned the last page and sat very still.", "au": "Anonymous"}],
    "12_31": [{"b": "It was ", "t": "half past twelve", "a": ", and the afternoon felt inexhaustible.", "au": "Anonymous"}],
    "13_36": [{"b": "", "t": "One thirty-six", "a": " in the afternoon. The last quiet hour before things changed.", "au": "Anonymous"}],
    "18_44": [{"b": "At ", "t": "sixteen minutes to seven", "a": " the kitchen light was still on.", "au": "Anonymous"}],
}

with open("app/author_clock.star", "r", encoding="ascii") as f:
    content = f.read()

all_keys = sorted(re.findall(r'"(\d\d_\d\d)":', content))
inserted = 0

for key in sorted(NEW_ENTRIES.keys()):
    if f'"{key}"' in content:
        print(f"SKIP {key} (already present)")
        continue

    entries = NEW_ENTRIES[key]
    lines = [f'    "{key}": [']
    for e in entries:
        lines.append(make_entry(e["b"], e["t"], e["a"], e["au"]) + ",")
    lines.append("    ],")
    block = "\n".join(lines) + "\n"

    # Find insertion point: before the next key in sorted order
    next_key = next((k for k in all_keys if k > key), None)
    if next_key:
        insert_before = f'    "{next_key}":'
        pos = content.find(insert_before)
        if pos == -1:
            print(f"ERROR: anchor not found for {key}")
            continue
        content = content[:pos] + block + content[pos:]
        all_keys = sorted(re.findall(r'"(\d\d_\d\d)":', content))  # refresh
        inserted += 1
        print(f"  inserted {key} before {next_key}")
    else:
        pos = content.rfind("}")
        content = content[:pos] + block + content[pos:]
        all_keys = sorted(re.findall(r'"(\d\d_\d\d)":', content))
        inserted += 1
        print(f"  inserted {key} at end")

with open("app/author_clock.star", "w", encoding="ascii") as f:
    f.write(content)

print(f"\nDone. Inserted {inserted} entries.")
