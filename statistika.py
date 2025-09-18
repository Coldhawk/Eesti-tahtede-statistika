from datasets import load_dataset
import matplotlib.pyplot as plt

# Dataset is made by Koppel, Kristina; Kallas, Jelena (2022).
# Eesti keele ühendkorpus 2021. DOI: 10.15155/3-00-0000-0000-0000-08E60L

# dataset only has one split, train, and is divided into dictionaries {"text": "SENTENCE"}.
# Loading the dataset as streaming, as the size of the dataset is over 20GB.

dataset = load_dataset(
    "siimh/estonian_corpus_2021",
    data_files="corpus_et_clean.jsonl",
    split="train",
    streaming=True,
)

# Loading a smaller sized dataset into a list
sample_count = 1e6
samples = []

# Sentence Loader
for i, sample in enumerate(dataset):
    samples.append(
        sample["text"].lower()
    )  # .lower so that it's easier to count letters
    if i >= sample_count - 1:
        break


def count_letters(sentence, char):
    return len([c for c in sentence if c == char])


alphabet = {letter: 0 for letter in "abdefghijklmnoprsšzžtuvõäöü"}

for sample in samples:
    for letter in alphabet.keys():
        alphabet[letter] += count_letters(sample, letter)

# Sort dictionary in decreasing order
sorted_alphabet = dict(sorted(alphabet.items(), key=lambda item: item[1], reverse=True))

for letter, count in sorted_alphabet.items():
    print(f"'{letter}': {count}")

# Calculate total counts and percentages
total_count = sum(sorted_alphabet.values())
percentages = {
    letter: (count / total_count) * 100 for letter, count in sorted_alphabet.items()
}

letters = list(percentages.keys())
counts = list(percentages.values())

fontsize = 16
plt.figure(figsize=(18, 12))
bars = plt.bar(letters, counts, color="skyblue")
plt.xlabel("Letters",fontsize = fontsize)
plt.ylabel("Percentage (%)", fontsize=fontsize)
plt.title("Letter Frequency as Percentage in Samples", fontsize=fontsize)
plt.xticks(fontsize = fontsize)
plt.grid(axis="y")

# Percentages above each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        f"{yval:.1f}%",
        ha="center",
        va="bottom",
        fontsize = fontsize
    )

plt.tight_layout()
plt.show()
