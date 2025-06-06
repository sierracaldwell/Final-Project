class DialogChoice:
    def __init__(self, text, next_node_id, image_path=None):
        self.text = text
        self.next_node_id = next_node_id
        self.image_path = image_path  # Optional path to image

class DialogNode:
    def __init__(self, node_id, text, choices, image_path=None):
        self.node_id = node_id
        self.text = text
        self.choices = choices
        self.image_path = image_path

class DialogGraph:
    def __init__(self, root_node_id, nodes):
        self.nodes = {node.node_id: node for node in nodes}
        self.current_node_id = root_node_id

    def current_node(self):
        return self.nodes[self.current_node_id]

    def make_choice(self, choice_index):
        current = self.current_node()
        if 0 <= choice_index < len(current.choices):
            self.current_node_id = current.choices[choice_index].next_node_id