import re
import unittest

LESS_INTERESTING = "___BELOW_IS_LESS_INTERESTING___"
EXTRA_INFO_HEADER = "[* extra info]"
MICROFORMAT_IGNORE = "`AI_IGNORE"
MICROFORMAT_TO_AI = "`TO_AI:"

TEST_for_markdown_to_scrapbox = "### A is level 3 header\n## B is level 2 header"


def markdown_to_scrapbox(text):
    """easy conversion from markdown to scrapbox
    >>> print(markdown_to_scrapbox(TEST_for_markdown_to_scrapbox))
    [* A is level 3 header]
    [** B is level 2 header]
    """
    # Replace '### ' with '[* ' and close with ']'
    text = re.sub(r"### (.+)", r"[* \1]", text)
    # Replace '## ' with '[** ' and close with ']'
    text = re.sub(r"## (.+)", r"[** \1]", text)
    return text


def extract_microformat_to_ai(input_str):
    """
    Extracts text enclosed between `TO_AI:` and backticks from the input string.

    Args:
        input_str (str): The input string containing the target text.

    Returns:
        str: The extracted text, or None if no match is found.

    Examples:
        >>> extract_microformat_to_ai("aaa`TO_AI: bbb`ccc")
        'bbb'

        >>> extract_microformat_to_ai("Some text without TO_AI")
        ...
    """
    pattern = r"`TO_AI: (.*?)`"
    match = re.search(pattern, input_str)
    if match:
        extracted_text = match.group(1)
        return extracted_text
    else:
        return None


def extract_previous_notes(prev_lines):
    """
    Extracts previous notes from a list of lines, filtering out less interesting and extra information headers.

    Args:
        prev_lines (list): List of lines containing previous notes and related information.

    Returns:
        str: A string containing the extracted previous notes.

    Raises:
        NotImplementedError: If a microformat TO_AI line is encountered.
    """
    if not prev_lines:
        return ""

    # Remove title line
    prev_lines.pop(0)

    # Check if the first line is less interesting, and skip if needed
    if prev_lines and prev_lines[0] == LESS_INTERESTING:
        prev_lines.pop(0)

    previous_notes_lines = []

    # Extract previous notes lines until less interesting, extra info header, or microformat is encountered
    for line in prev_lines:
        if line in [LESS_INTERESTING, EXTRA_INFO_HEADER]:
            break
        if MICROFORMAT_IGNORE in line:
            continue
        if MICROFORMAT_TO_AI in line:
            prompt = extract_microformat_to_ai(line)
            raise NotImplementedError("Microformat TO_AI is not yet implemented")

        previous_notes_lines.append(line)

    # Combine extracted lines into a string
    previous_notes = "\n".join(previous_notes_lines)

    return previous_notes


class TestExtractPreviousNotes(unittest.TestCase):
    def test_extract_previous_notes(self):
        prev_lines = [
            "Title",
            LESS_INTERESTING,
            "Some notes...",
            EXTRA_INFO_HEADER,
            "More notes...",
        ]

        extracted_notes = extract_previous_notes(prev_lines)

        expected_notes = "Some notes..."
        self.assertEqual(extracted_notes, expected_notes)

    def test_extract_previous_notes_ignore(self):
        prev_lines = [
            "Title",
            LESS_INTERESTING,
            "Some notes...",
            "`AI_IGNORE: This line should be ignored`",
            EXTRA_INFO_HEADER,
            "More notes...",
        ]

        extracted_notes = extract_previous_notes(prev_lines)

        expected_notes = "Some notes..."
        self.assertEqual(extracted_notes, expected_notes)

    def test_extract_previous_notes_with_microformat(self):
        prev_lines = [
            "Title",
            "AAA",
            LESS_INTERESTING,
            "BBB",
            EXTRA_INFO_HEADER,
            "More notes...",
        ]

        extracted_notes = extract_previous_notes(prev_lines)

        expected_notes = "AAA"
        self.assertEqual(extracted_notes, expected_notes)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
