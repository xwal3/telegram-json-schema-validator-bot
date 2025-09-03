"""
    def is_grounded(self, reply: str, tool_output: str, fuzzy_threshold: float = 0.8) -> dict:
        tool_tokens = tool_output.split()
        reply_tokens = reply.split()

        matched_tokens = []
        unmatched_tokens = []


        def fuzzy_match(a: str, b: str) -> bool:
            return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= fuzzy_threshold


        def extract_numbers_units(text: str) -> list:
            return re.findall(r'\d+\.?\d*\s*°?[a-zA-Z]*', text)


        for token in tool_tokens:
            found = token in reply_tokens or any(fuzzy_match(token, r) for r in reply_tokens)
            if found:
                matched_tokens.append(token)
            else:
                unmatched_tokens.append(token)

        numbers_units = extract_numbers_units(tool_output)
        for nu in numbers_units:
            if nu in reply:
                if nu not in matched_tokens:
                    matched_tokens.append(nu)
                if nu in unmatched_tokens:
                    unmatched_tokens.remove(nu)

        grounded_ratio = len(matched_tokens) / max(1, len(tool_tokens))
        grounded = grounded_ratio > 0.5  

        return {
            'grounded': grounded,
            'matched_tokens': matched_tokens,
            'unmatched_tokens': unmatched_tokens,
            'grounded_ratio': grounded_ratio
        }


"""