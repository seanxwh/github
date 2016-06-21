class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST(object):
    def __init__(self, root):
        self.root = Node(root)

    def insert(self, new_val):
        self.findAndInsert(self.root, new_val)
        # pass

    def search(self, find_val):
        toggle = self.recursiveSearch(self.root, find_val )
        return toggle or False

    def delete(self,val):
        self.searchAndDeleteNode(self.root, val, self.root)

        #case 1, found the node in the leaf -> aka bottom -> parent node's next point to None, delete current node
        #case 2, has one child node -> point parent's next to child node, delete current node
        #case 3, has 2 child nodes -> replace the current node with the left most descendent (can be at any level) node from the right child node

    def searchAndDeleteNode(self, node, val, parent):
        nodeSideInParent=None
        if val == node.value:
            if node == parent.left:
                   nodeSideInParent = "L"
            elif node == parent.right:
                   nodeSideInParent = "R"
            #c1
            if not node.left and not node.right:
                if nodeSideInParent == "L":
                    parent.left = None
                elif nodeSideInParent == "R":
                    parent.right = None
            #c2
            elif node.left and not node.right:
                if nodeSideInParent == "L":
                    parent.left = node.left
                elif nodeSideInParent == "R":
                    parent.right = node.left
            elif node.right and not node.left:
                if nodeSideInParent == "L":
                    parent.left = node.right
                elif nodeSideInParent == "R":
                    parent.right = node.right

            #c3
            elif node.right and node.left:

                if  nodeSideInParent==None: # the root node
                    val = self.findAndDeleteLeftMostDescendent(node.right, node.right)
                    parent.value = val.value
                    parent.right = val.right

                elif nodeSideInParent == "L":
                    parent.left = self.findAndDeleteLeftMostDescendent(node.left, node)
                elif nodeSideInParent == "R":
                    parent.right = self.findAndDeleteLeftMostDescendent(node.left, node)


        elif val != node.value:
            if node.left or node.right:
                for branch in [node.left, node.right]:
                    if branch:
                        self.searchAndDeleteNode(branch, val, node)


    def findAndDeleteLeftMostDescendent(self, node, parent):
        if not node.left:
            parent.left = None
            node.right = parent.right
            return node
        elif node.left:
            self.findAndDeleteLeftMostDescendent(node.left, node)


    def recursiveSearch(self, node, val):
        if val == node.value:
            return True
        elif node.left or node.right:
            for branch in [node.left, node.right]:
                if branch != None:
                    value = self.recursiveSearch(branch, val)
                    if value == True:
                        return value
        else:
            return False

    def findAndInsert(self, node, val):
        if node.value == val:
            return
        elif node.value > val:
            if node.left == None:
                node.left = Node(val)
            else: self.findAndInsert(node.left, val)
        elif node.value < val:
            if node.right == None:
                node.right = Node(val)
            else: self.findAndInsert(node.right, val)

    def print_tree(self):
        # """Print out all tree nodes
        # as they are visited in
        # a pre-order traversal."""
        startingList = []
        tree = self.preorder_print(self.root, startingList)
        print_val = '-'.join(map(str, tree))
        return print_val

    def preorder_print(self, start, traversal):
    # """Helper method - use this to create a
    # recursive print solution."""
        if start.value:
            traversal.append(start.value)
        if start.left or start.right:
            for branch in [start.left, start.right]:
                if branch != None:
                    traversal = self.preorder_print(branch,traversal)
        return traversal
# Set up tree
tree = BST(5)

# Insert elements
tree.insert(2)
tree.insert(1)
tree.insert(7)
tree.insert(6)
tree.insert(4)
tree.insert(9)
tree.insert(3)

# Check search
# Should be True
print tree.print_tree()
print tree.search(5)
# print tree.print_tree()
# Should be False
print tree.search(8)
print tree.print_tree()

tree.delete(2)
print tree.print_tree()
tree.insert(2)
print tree.print_tree()
tree.delete(1)
print tree.print_tree()
tree.insert(1)
print tree.print_tree()
tree.delete(3)
print tree.print_tree()
tree.delete(7)
print tree.print_tree()
tree.delete(5)
print tree.print_tree()
