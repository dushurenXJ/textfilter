
class DFAFilter:

    def __init__(self):
        self.key_dict = {}
        self.end = '\x00'

    def add(self, keyword):
        keyword = keyword.strip()
        if not keyword:
            return
        temp_dict = self.key_dict
        for index in range(len(keyword)):
            if keyword[index] in temp_dict:
                temp_dict = temp_dict[keyword[index]]
            else:
                for i in range(index, len(keyword)):
                    temp_dict[keyword[i]] = {}
                    temp_dict = temp_dict[keyword[i]]
                temp_dict[self.end] = 0
                break

    def parse(self, file_path):
        file_obj = open(file_path, 'r', encoding='utf-8')
        for keyword in file_obj:
            self.add(keyword)


    def filter(self, content, repl='*'):
        result = []
        start = 0
        while start < len(content):
            step_length = 0
            curr_dict = self.key_dict

            for char in content[start:]:
                if char in curr_dict:
                    step_length += 1
                    if self.end not in curr_dict[char]:
                        curr_dict = curr_dict[char]
                        if start == len(content) - 1:
                            result.append(repl * step_length)
                    else:
                        result.append(repl * step_length)
                        start += step_length - 1
                        break
                else:
                    result.append(content[start])
                    break
            start += 1
        return ''.join(result)


if __name__ == '__main__':
    filter = DFAFilter()
    filter.add('你好')
    filter.add('你好啊')
    filter.add('好人好报')
    print(filter.key_dict)
    print(filter.filter('你好是一个好人，你好啊，我知道你好'))

