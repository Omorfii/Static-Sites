class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = []
        if not self.props:
            return ""
        for key, value in self.props.items():
            result.append(f' {key}="{value}"')
        return "".join(result)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("A leaf node must have a value")
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A parent node must have a tag")
        if not self.children:
            raise ValueError("A parent node must have a children")
        parent_result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            parent_result += child.to_html()
        parent_result += f"</{self.tag}>"
        return parent_result 