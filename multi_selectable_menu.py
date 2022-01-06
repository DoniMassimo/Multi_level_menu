# use python 3.8.10 or less
# librery to install to use this library
#   curtsies -> terminal command : 'pip install curtsies'

import support_library_v1 as sl
from curtsies import Input


def get_list_index(list, index):
    if index < len(list) and index >= 0:
        return list[index]
    else: return False

class Node:  # simply node
    def __init__(self, data) -> None:
        self._data = data
        self._children = []
        self._parent = None

    def add_child(self, child):   # ciao     
        child._parent = self
        self._children.append(child)


class Node_menu(Node): 
    # node with functions for creating tree menus
    # every func works locally, so we can call func for every node and not only for the root
    def __init__(self, data) -> None:
        super().__init__(data)

    def get_level(self):
        level = 0
        par = self._parent
        while par:
            level += 1
            par = par._parent
        return level

    def get_data(self):
        return self._data

    def print_tree(self, sel_item_address, index=0, tab='', selected_item=True): # sel = selected
        sel_char = '#'
        def_char = '-'
        if selected_item==True and (get_list_index(sel_item_address, index) == -1 or index == len(sel_item_address)):             
            print(f'{tab}{sel_char}{self._data}')            
        else:
            print(f'{tab}{def_char}{self._data}')
        if self._children:
            for i, child in enumerate(self._children):
                if i == sel_item_address[index] and selected_item:
                    child.print_tree(sel_item_address, index+1, tab=tab+'  ', selected_item=True)
                else:
                    child.print_tree(sel_item_address, index+1, tab=tab+'  ', selected_item=False)

    def get_max_level(self, level=-1, record_level=-1):
        level += 1
        if level > record_level:
            record_level = level
        if self._children:                 # se hai figli
            for child in self._children:   # ciclo dei figli
                record_level = child.get_max_level(level, record_level)
        return record_level

    def check_address(self, address, index=0):  # ? da riscrivere
        if self._children:
            if (address[index] < len(self._children)):
                if index < len(address)-1:
                    if address[index+1] == -1:
                        return True
                if index == len(address)-1:
                    return True
                return self._children[address[index]].check_address(address, index+1)
            else:
                return False
        else: 
            return False


class Multi_level_menu:
    # sel_char : char for the selected items / if you want to creat tree menu

    def __init__(self, menu_map:str, default_pre_items_char='-', selected_pre_items_char='#') -> None:
        self.__root = self.__create_tree(menu_map)
        self.sel_char = selected_pre_items_char[0]
        self.def_char = default_pre_items_char[0]
        self.__address = self.__calculate_address_lenght()        

    def __create_tree(self, tree_map) -> Node_menu:
        def create_branchs(branch_map, parent_node):            
            opened_brachets = 0
            open_ = False       # true whene there is a brachets
            str_branch = ''
            for i, char in enumerate(branch_map):
                if char == '(': 
                    opened_brachets += 1
                    open_ = True
                elif char == ')': 
                    opened_brachets -= 1                
                if (char == '-' and opened_brachets == 0 or i == len(branch_map)-1): 
                    if i == len(branch_map)-1: str_branch += char
                    if open_ == True:       # qui c'è un nodo con altri sotto-nodi
                        child_node = Node_menu(str_branch[:str_branch.find('(')])
                        create_branchs(str_branch[str_branch.find('(')+1:-1], child_node)
                        parent_node.add_child(child_node)
                        open_ = False                          
                    else:       # nodo finale
                        parent_node.add_child(Node_menu(str_branch))
                    str_branch = ''
                    continue       
                str_branch += char            
        root = Node_menu('@')
        create_branchs(tree_map, root)       
        return root
                           
    def __calculate_address_lenght(self):
        address = [0]
        for i in range(self.__root.get_max_level()-1):
            address.append(-1)
        return address

    def __change_adress(self, movement='none'):
        address_copy = self.__address.copy()
        movement = movement.upper()
        if movement == 'UP' or movement == 'DOWN':
            for i in range(len(self.__address)):
                if self.__address[i] == -1:
                    if movement == 'UP' and self.__address[i-1] > 0:
                        self.__address[i-1] = self.__address[i-1] - 1
                        break
                    elif movement == 'DOWN':
                        self.__address[i-1] = self.__address[i-1] + 1
                        break

                elif i+1 == len(self.__address):
                    if movement == 'UP' and self.__address[i] > 0:
                        self.__address[i] = self.__address[i] - 1
                        break
                    elif movement == 'DOWN':
                        self.__address[i] = self.__address[i] + 1
                        break

        elif movement == 'RIGHT' or movement == 'LEFT':
            for i in range(len(self.__address)):
                if self.__address[i] == -1 and movement == 'RIGHT':
                    self.__address[i] = 0
                    break
                elif self.__address[i] == -1 and movement == 'LEFT' and i-1 != 0:
                    self.__address[i-1] = -1
                    break
                elif i+1 == len(self.__address):
                    self.__address[i] = -1
                    break

        if self.__root.check_address(self.__address) == False: self.__address = address_copy

    def start_menu(self):  # for selcte item click 'KEY_RIGHT' or enter / it return the index ant the content of chosing item
        self.__change_adress()
        with Input(keynames='curses') as input_generator:
            sl.clear()
            print(f'{self.__address}')
            print()
            self.__root.print_tree(sel_item_address=self.__address)
            for _input in input_generator:
                if _input == 'KEY_UP':
                    self.__change_adress('up')
                elif _input == 'KEY_DOWN':
                    self.__change_adress('down')
                elif _input == 'KEY_RIGHT':
                    self.__change_adress('right')
                elif _input == 'KEY_LEFT':
                    self.__change_adress('left')
                elif _input == '\n':
                    break

                sl.clear()
                print(f'{self.__address}')
                print()
                self.__root.print_tree(sel_item_address=self.__address)



if __name__ == '__main__':    
    sl.clear()
    m = Multi_level_menu(menu_map='fi(ff-ss)-sec(cc-dd(rr(ww-ee-tt)-mm))')    
    m.start_menu()    
    pass
