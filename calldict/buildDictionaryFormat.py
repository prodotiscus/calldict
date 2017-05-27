#!/usr/bin/python3
import requests
import re
import difflib
import urllib.parse

class examples:
    def __init__(self):
        self.ex = []
    def add_example(self, url, title, props):
        self.ex.append([url, title, props])
    def find_substring_index(self, string, substr):
        ret = []
        for c in range(len(string)):
            if string[c] == substr[0]:
                if string[c:c + len(substr)] == substr:
                    ret.append((c, c + len(substr)))
        return ret
    def del_all(self, string, to_del):
        for td in to_del:
            string = string.replace(td, '')
        return string
    def pages_average(self, index, pages, to_del):
        simil = []
        for j in range(0, len(pages), 2):
            if j + 1 == len(pages):
                break
            try:
                simil.append(
                    difflib.SequenceMatcher(
                        a = self.del_all(pages[j][index], to_del),
                        b = self.del_all(pages[j + 1][index], to_del)
                    ).ratio()
                )
            except IndexError:
                return 1.0
        return sum(simil) / len(simil)
    def string_clear(self, string):
        if string == '':
            return string
        string = string.replace('\t', '')
        while '  ' in string or '\t' in string or '\n' in string:
            string = string.replace('  ', '')
            string = string.replace('\t', '')
            string = string.replace('\n', '')
        try:
            if string[0] in (' ', '\t', '\n'):
                string = string[1:]
            if string[-1] in (' ', '\t', '\n'):
                string = string[:-1]
            return string
        except IndexError:
            return ''
    def contains_lonely(self, string, pattern):
        b = '! @ # $ % ^ & * ( ) - _ = + \\ | / < > , . ? " \''
        b += '~ ` { } [ ] : ; " №'
        b_symb = b.split()
        b_symb.append(' ')
        l_string = len(string)
        l_pattern = len(pattern)
        matched = 0
        while pattern in string:
            p_index = string.index(pattern)
            if p_index > 0 and p_index < l_string - 1:
                if string[p_index - 1] in b_symb and string[p_index + l_pattern] in b_symb:
                    matched += 1
            elif p_index == 0:
                if string[p_index + l_pattern + 1] in b_symb:
                    matched += 1
            elif p_index == len_string - 1:
                if string[p_index - 1] in b_symb:
                    matched += 1
            string = string.replace(pattern, '', 1)
        return matched
    def make_template(self, string, word):
        string = string.replace('@', '\\@')
        word_split = re.split('\s+', word)
        for j in range(len(word_split)):
            string = string.replace(urllib.parse.quote(word_split[j]), '@A')
            string = string.replace(word_split[j], '@' + str(j))
        string = re.sub('(@A[_%\dA-Z]*)+', '@A', string)
        return string
    def wrap_check(self, line, content, category):
        wraps = []
        mode = 'full'
        modes = ['full', 'w/brackets']
        cur_content = content
        for m in modes:
            if m == 'full':
                pass
            elif m == 'w/brackets':
                cur_content = self.string_clear(cur_content)[1:-1]
            # tag check
            tag_wraps = re.findall(r'<[^>]+>' + cur_content + r'<\/[^>]+>', line)
            if len(tag_wraps) > 0:
                current_tw = self.make_template(tag_wraps[0], cur_content)
                return {
                    'mode' : m,
                    'template' : current_tw
                }
            # post-tag check
            post_tags = re.findall(r'<[^>]+>' + cur_content + r'[\s\t\n]*$', line)
            if len(post_tags) > 0:
                matching_pattern = self.string_clear(post_tags[0])
                return {
                    'mode' : m,
                    'template' : self.make_template(matching_pattern, cur_content)
                }
        return False
    def between_lines(self, pair, join = True):
        proc = self.cache[pair[0]:pair[1] + 1]
        return '\n'.join(proc) if join else proc
    def process(self):
        pages = []
        to_del = []
        for e in self.ex:
            markup = requests.get(e[0]).text
            pages.append(markup.split('\n'))
            to_del.append(e[1])
            for p in e[2]:
                to_del.append(p)
        type_templates = []
        for q in range(len(pages)):
            borders = []            
            self.cache = pages[q]
            for j in range(len(pages[q])):
                if self.pages_average(j, pages, to_del) < 0.9:
                    borders.append(
                        (j, self.string_clear(pages[q][j]))
                    )
            selected_borders = []
            border_props = {}        
            for j in range(len(borders)):
                if j + 1 == len(borders):
                    break
                border_props[borders[j][0]] = 0
                for pattern in self.ex[q][2]:                
                    border_cl = self.contains_lonely(
                        self.between_lines(
                            (borders[j][0], borders[j + 1][0])
                        ),
                        pattern
                    )
                    border_props[borders[j][0]] += border_cl
            row = list(set((list(border_props))))
            priority = sorted(border_props, key=border_props.get)
            priority = list(reversed(priority))
            last_index = len(self.cache) - 1
            ignore = {
                'html-tags' : ['meta']
            }
            len_priority = len(priority)
            for j in range(len_priority):
                ind = priority[j]
                next_ind = priority[j + 1] if j < len_priority - 1 else last_index
                for c in self.between_lines((ind, next_ind), join = False):
                    ignored = False
                    c = self.string_clear(c)
                    if 'html-tags' in ignore:
                        for ignored_tag in ignore['html-tags']:
                            if re.search('<\s*' + ignored_tag, c):
                                ignored = True
                                break
                    if ignored:
                        continue
                    for pattern in self.ex[q][2]:
                        swc = self.wrap_check(c, pattern, self.ex[q][2][pattern])
                        if swc:
                            type_templates.append((self.ex[q][2][pattern], swc))
        return type_templates