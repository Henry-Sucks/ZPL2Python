class IndTreeNode:
        def  __init__(self, value):
            self.code = ""
            self.value = value
            self.children = []

            # 为什么是-1？因为top_node是一个空节点，需要耗费一次层数
            self.level = -1
            

        def add_child(self, child_node):
            self.children.append(child_node)

        def set_children(self, items):
            if isinstance(items, list):
                for item in items:
                    self.set_children(item)
            elif isinstance(items, IndTreeNode):
                    self.add_child(items)


        def set_value(self, value):
            self.value = value

        def get_children(self):
            return self.children
        
        def get_indentation(self):
            cur_indentation = ""
            for i in range(self.level):
                cur_indentation += "\t"

            return cur_indentation
        
        
        def dfs(self, cur_level):
            # 访问当前节点
            ## 将缩进+value中代码放入value中
            ## 增加缩进层数
            self.level = cur_level
            self.value = f"{self.get_indentation()}{self.value}"
            self.level += 1


            ## 遍历子节点，加上子节点返回的代码
            for child in self.children:
                
                self.value += child.dfs(self.level)

            return self.value
        
        def build_code(self):
            self.code = self.dfs(self.level)
            return
        
        def get_code(self):
            return self.code
            
            
        def __repr__(self):
            children_repr = ', '.join(repr(child) for child in self.children)
            return f"IndTreeNode(\"{self.value}\", [{children_repr}])"