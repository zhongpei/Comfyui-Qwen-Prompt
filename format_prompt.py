import regex as re
import unicodedata

brackets_opening = '([{<'
brackets_closing = ')]}>'

# base = r'(?:\\[()\[\]{}<>]|[^,(){}\[\]{}<>])+'
# paren = r'\(+' + base + r'\)+'
# square = r'\[+' + base + r'\]+'
# curly = r'{+' + base + r'}+'
# angle = r'<+' + base + r'>+'


# re_tokenize = re.compile('|'.join([base, paren, square, curly, angle]))
re_tokenize = re.compile(r',')
re_brackets_fix_whitespace = re.compile(r'([\(\[{<])\s*|\s*([\)\]}>}])')
re_opposing_brackets = re.compile(r'([)\]}>])([([{<])')
re_networks = re.compile(r'<.+?>')
re_bracket_open = re.compile(r'[(\[]')
re_brackets_open = re.compile(r'\(+|\[+')
re_brackets_closing = re.compile(r'\)+|\]+')
# re_colon_spacing_composite = re.compile(r'(?P<A>[^:]*?)\s*?(?P<COLON>:)\s*?(?P<B>\S*)(?P<S>\s*)(?(S)\s*?)(?P<AND>AND)')
re_colon_spacing_composite = re.compile(r'\s*(:)\s*(?=\d*?\.?\d*?\s*?AND)')
re_colon_spacing = re.compile(r'\s*(:)\s*')
# re_colon_spacing = re.compile(r'(?P<A>[^:]*?)\s*?(?P<COLON>:)\s*?(?P<B>\S+)(?P<S>\s*)(?(S)\s*?)')
re_colon_spacing_comp_end = re.compile(r'(?<=AND[^:]*?)(:)(?=[^:]*$)')
re_comma_spacing = re.compile(r',+')
re_paren_weights_exist = re.compile(r'\(.*(?<!:):\d.?\d*\)+')
re_is_prompt_editing = re.compile(r'\[.*:.*\]')
re_is_prompt_alternating = re.compile(r'\[.*|.*\]')
re_is_wildcard = re.compile(r'{.*}')
re_AND = re.compile(r'(.*?)\s*(AND)\s*(.*?)')
re_alternating = re.compile(r'\s*(\|)\s*')


def get_bracket_closing(c: str):
    return brackets_closing[brackets_opening.find(c)]


def get_bracket_opening(c: str):
    return brackets_opening[brackets_closing.find(c)]


def normalize_characters(data: str):
    return unicodedata.normalize("NFKC", data)


def tokenize(data: str):
    return re_tokenize.findall(data)


def remove_whitespace_excessive(prompt: str):
    return ' '.join(prompt.split())

    # pruned = [' '.join(token.strip().split()) for token in tokens]
    # pruned = list(filter(None, pruned))
    # return pruned


def align_brackets(prompt: str):
    def helper(match: re.Match):
        return match.group(1) or match.group(2)

    return re_brackets_fix_whitespace.sub(helper, prompt)

    # return list(map(lambda token : re_brackets_fix_whitespace.sub(helper, token), tokens))


def space_AND(prompt: str):
    def helper(match: re.Match):
        return ' '.join(match.groups())

    return re_AND.sub(helper, prompt)


def align_colons(prompt: str):
    def normalize(match: re.Match):
        return match.group(1)

    def composite(match: re.Match):
        return ' ' + match.group(1)

    def composite_end(match: re.Match):
        # print(f'match: {match}')
        return ' ' + match.group(1)

    ret = re_colon_spacing.sub(normalize, prompt)
    ret = re_colon_spacing_composite.sub(composite, ret)
    ret = re_colon_spacing_comp_end.sub(composite_end, ret)
    return ret

    # def helper(match: re.Match):
    #     if match.group('AND'):
    #         return f"{match.group('A')} :{match.group('B')} AND"

    #     return f"{match.group('A')}:{match.group('B')}"

    # def edge_case(match: re.Match):
    #     # edge case where if composite with weight at end, fix alignment
    #     if match.group('AND'):
    #         return ' '.join(match.group('AND', 2)) + ' ' + ''.join(match.group(3, 4))

    # ret = re_colon_spacing.sub(helper, prompt)
    # return re_colon_spacing_comp_end.sub(edge_case, ret)

    # def fix_ending_compositing(s: str):
    #     # edge case where if composite, weight isn't followed by AND, need to
    #     # check backwards and check if needs to fix alignment
    #     match = re_colon_spacing_comp_end.match(s)
    #     if match.group('AND'):
    #         return ' '.join(match.group(1, 2)) + ' ' + ''.join(match.group(3, 4))

    # ret = re_colon_spacing.sub(helper, prompt)
    # return fix_ending_compositing(ret)


def align_commas(prompt: str):
    split = re_comma_spacing.split(prompt)
    split = map(str.strip, split)
    split = filter(None, split)
    return ', '.join(split)


# def brackets_to_weights(tokens: list, power: int = 0):
#     print(tokens)
#     ret = []
#     re_opening_paren = re.compile('\([^\(]')
#     re_opening_square = re.compile('\[[^\[]')

#     for token in tokens:
#         if re_opening_paren.match(token):
#             pass


# Assumes colons have already been spaced corretly
# def normalize(token:str):
#     pass
# if not re_brackets_open.match(token):
#     return token

# brackets = re_brackets_open.match(token).group(0)
# power = len(brackets) if not brackets[0] == '[' else -len(brackets)
# depth = abs(power)

# if (re_paren_weights_exist.search(token) or
#     re_is_prompt_editing.search(token) or
#     re_is_wildcard.search(token) or
#     re_is_prompt_alternating.search(token)):
#     return str(brackets[0] + token[depth:len(token)-depth] + get_bracket_closing(brackets[0]))     # just return normalized bracketing

# weight = 1.1 ** power
# return '(' + token[depth:len(token)-depth] + ('' if token[-depth-1:-depth] == ':' else ':') + f'{weight:.2f}' + ')'


# return list(map(normalize, tokens))


def extract_networks(tokens: list):
    return list(filter(lambda token: re_networks.match(token), tokens))


def remove_networks(tokens: list):
    return list(filter(lambda token: not re_networks.match(token), tokens))


def remove_mismatched_brackets(prompt: str):
    stack = []
    pos = []
    ret = ''

    for i, c in enumerate(prompt):
        if c in brackets_opening:
            stack.append(c)
            pos.append(i)
            ret += c
        elif c in brackets_closing:
            if not stack:
                continue
            if stack[-1] == brackets_opening[brackets_closing.index(c)]:
                stack.pop()
                pos.pop()
                ret += c
        else:
            ret += c

    while stack:
        bracket = stack.pop()
        p = pos.pop()
        ret = ret[:p] + ret[p + 1:]

    return ret


# Tokenizing is extremely tedious and perhaps unecessary...
# def tokenize_nested(prompt: str):
#     """
#     Tokenizes the prompt based on commas, brackets, and parenthesis.
#     """
#     result = []
#     re_dividers = re.compile(r'(?<!\\)([\(\)\[\],<>{}])')

#     pos = 0
#     while pos < len(prompt):
#         match = re_dividers.search(prompt, pos)
#         # we know we're at the end of the string when we can't match
#         if match is None:
#             substring = prompt[pos:].strip()
#             if substring:
#                 result.append(substring)
#             break

#         # add up to the previous token up to excluding our matched position
#         substring = prompt[pos:match.start()].strip()
#         if substring:
#             result.append(prompt[pos:match.start()].strip())
#             if prompt[match.start()] in '}>':    # brackets don't get added, so this corrects for it
#                 result[-1] = get_bracket_opening(prompt[match.start()]) + result[-1] + prompt[match.start()]

#         # if comma, move pos past it
#         if prompt[match.start()] in ',<>{}':     
#             pos = match.end()

#         # finally deal with real nested stuff
#         elif prompt[match.start()] in '[(':
#             nested_result, length = tokenize_nested(prompt[match.end():])    # recurses with s, the end of match onwards
#             nested_result[0] = prompt[match.start()] + nested_result[0]
#             result.append(nested_result)
#             pos = match.end() + length
#         elif prompt[match.start()] in '])':                                  
#             result[-1] = result[-1] + prompt[match.start()]                  # return from recurse, including the
#             return result, match.end()                                  # end of the match to correct position
#     return result


# def flatten_tokens(tokens: list):
#     ret = []
#     for token in tokens:
#         if isinstance(token, list):
#             ret.extend(flatten_tokens(token))
#         else:
#             ret.append(token)

#     return ret


def space_bracekts(prompt: str):
    def helper(match: re.Match):
        # print(' '.join(match.groups()))
        return ' '.join(match.groups())

    # print(prompt)
    return re_opposing_brackets.sub(helper, prompt)


def align_alternating(prompt: str):
    def helper(match: re.Match):
        return match.group(1)

    return re_alternating.sub(helper, prompt)


def bracket_to_weights(prompt: str):
    """
    when scanning, we need a way to ignore prompt editing, composable, and alternating
    we still need to weigh their individual words within them, however...

    use a depth counter to ensure that we find closing brackets

    the problem is that as we modify the string, we will be changing it's length,
    which will mess with iterations...
        we can simply edit the string backwards, that way the operations don't effect
        the length of the parts we're working on... however, if we do this, then we can't
        remove consecutive brackets of the same type, we we would need to remove bracketing
        to the left of the part of the string we're working on.
    
    well, i think we should be fine with a while pos != end of string, and if we find
    a weight to add, break from the enumerate loop and resume at position to re-enumerate
    the new string

    go until we reach a [(, ignore networks < and wildcards {
    if (
        count if consecutive repeating bracket
        look forward to find its corresponding closing bracket
        check if those closing brackets are also consecutive
        add weighting at the end
        remove excessive bracket
        convert bracket to ()
    if [
        count if consecutive repeating bracket
        look forward
            if we find a : or |, return/break from this weight search
            else, to find its corresponding closing bracket
            check if those closing brackets are also consecutive
            add weighting at the end
            remove excessive bracket
            convert bracket to ()

    IF BRACKETS ARE CONSECUTIVE, AND AFTER THEIR SLOPE, BOTH THEIR 
    INNER-NEXT DEPTH ARE THE SAME, IT IS A WEIGHT.
    
    Example using map_depth.
    c, ((a, b))
       ((    ))
    00012222210
    ---^^----vv
   2     ____  2
   1    /===>\ 1
   0___/=====>\0 
    Because 01 can meet on the other side, these are matching
    
    c, (a, (b))
       (   ( ))
    00011112210
    ---^---^-vv
   2        _  2
   1    ___/>\ 1
   0___/=====>\0
    0 and 1 match, but since gradients are not exactly mirrored,
    thier weights should not be combined.

    c, ((a), b)
       (( )   )
    00012211110
    ---^^-v---v
   2     _     2
   1    /=\___ 1
   0___/=====>\0
    Similar idea to above example.
    
    c, ((a), ((b)))
       (( )  (( )))
    000122111233210
    ---^^-v--^^-vvv
   3           _   3
   2     _    />\  2
   1    />\__/==>\ 1
   0___/=========>\0
    Tricky one. Here, 01 open together, so there's a potential that their
    weights should be combined if they close together, but instead 1 closes
    early. We only need to check for closure initial checking depth - 1.
   
    """
    re_existing_weight = re.compile(r'(:\d+.?\d*)[)\]]$')
    depths, gradients, brackets = get_mappings(prompt)

    pos = 0
    ret = prompt
    gradient_search = []

    while pos < len(ret):
        current_position = ret[pos:]
        if ret[pos] in '([':
            open_bracketing = re_brackets_open.match(ret, pos)
            consecutive = len(open_bracketing.group(0))
            gradient_search = ''.join(map(str, reversed(range(int(depths[pos]) - 1, int(depths[pos]) + consecutive))))
            is_square_brackets = True if '[' in open_bracketing.group(0) else False

            insert_at, weight, valid_consecutive = get_weight(
                ret,
                gradients,
                depths,
                brackets,
                open_bracketing.end(),
                consecutive,
                gradient_search,
                is_square_brackets)

            # Check if weight already exists
            if weight:
                if re_existing_weight.search(ret[:insert_at + 1]):
                    ret = ret[:open_bracketing.start()] + '(' + ret[
                                                                open_bracketing.start() + valid_consecutive:insert_at] + ')' + ret[
                                                                                                                               insert_at + consecutive:]
                else:
                    ret = ret[:open_bracketing.start()] + '(' + ret[
                                                                open_bracketing.start() + valid_consecutive:insert_at] + f':{weight:.2f}' + ')' + ret[
                                                                                                                                                  insert_at + consecutive:]
                # offset = len(str(f'{weight:.2f}'))

            depths, gradients, brackets = get_mappings(ret)
            pos += 1

        match = re_bracket_open.search(ret, pos)

        if not match:  # no more potential weight brackets to parse
            return ret

        pos = match.start()


def depth_to_map(s: str):
    ret = ''
    depth = 0
    for c in s:
        if c in '([':
            depth += 1
        if c in ')]':
            depth -= 1
        ret += str(depth)
    return ret


def depth_to_gradeint(s: str):
    ret = ''
    for c in s:
        if c in '([':
            ret += str('^')
        elif c in ')]':
            ret += str('v')
        else:
            ret += str('-')
    return ret


def filter_brackets(s: str):
    return ''.join(list(map(lambda c: c if c in '[]()' else ' ', s)))


def get_mappings(s: str):
    return depth_to_map(s), depth_to_gradeint(s), filter_brackets(s)


def calculate_weight(d: str, is_square_brackets: bool):
    return 1 / 1.1 ** int(d) if is_square_brackets else 1 * 1.1 ** int(d)


def get_weight(prompt: str, map_gradient: list, map_depth: list, map_brackets: list, pos: int, ctv: int,
               gradient_search: str, is_square_brackets: bool = False):
    '''
    Returns 0 if bracket was recognized as prompt editing, alternation, or composable
    '''
    # CURRENTLY DOES NOT TAKE INTO ACCOUNT COMPOSABLE?? DO WE EVEN NEED TO?
    # E.G. [a AND B :1.2] == (a AND B:1.1) != (a AND B:1.1) ????
    while pos + ctv <= len(prompt):
        if ctv == 0:
            return prompt, 0, 1
        a, b = pos, pos + ctv
        if prompt[a] in ':|' and is_square_brackets:
            if map_depth[-2] == map_depth[a]:
                return prompt, 0, 1
            if map_depth[a] in gradient_search:
                gradient_search = gradient_search.replace(map_depth[a], '')
                ctv -= 1
        elif (map_gradient[a:b] == 'v' * ctv and
              map_depth[a - 1:b] == gradient_search):
            return a, calculate_weight(ctv, is_square_brackets), ctv
        elif ('v' == map_gradient[a] and
              map_depth[a - 1:b - 1] in gradient_search):
            narrowing = map_gradient[a:b].count('v')
            gradient_search = gradient_search[narrowing:]
            ctv -= 1
        pos += 1

    raise Exception(f'Somehow weight index searching has gone outside of prompt length with prompt: {prompt}')


def format_prompt(prompt):
    if not prompt or prompt.strip() == '':
        return prompt

    # Clean up the string
    prompt = normalize_characters(prompt)
    prompt = remove_mismatched_brackets(prompt)

    # Clean up whitespace for cool beans
    prompt = remove_whitespace_excessive(prompt)
    prompt = align_brackets(prompt)
    prompt = space_AND(prompt)  # for proper compositing alignment on colons
    prompt = space_bracekts(prompt)
    prompt = align_colons(prompt)
    prompt = align_commas(prompt)
    prompt = align_alternating(prompt)
    prompt = bracket_to_weights(prompt)

    # Further processing for usability
    # prompt = brackets_to_weights(prompt)
    # networks = extract_networks(tokens)
    # tokens = remove_networks(tokens)
    # tokens.extend(networks)

    # tokens = flatten_tokens(tokens)
    # ret.append(', '.join(list(tokens)))
    return prompt


class FormatPrompt:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",
                         {
                             "multiline": True
                         }),

            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_prompt"
    OUTPUT_NODE = True
    CATEGORY = "Qwen"

    def get_prompt(self, text: str, ) -> tuple[str]:
        return (format_prompt(text),)

NODE_CLASS_MAPPINGS = {
    "FormatPrompt": FormatPrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FormatPrompt": "Format Prompt",
}