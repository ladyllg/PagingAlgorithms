""" Código por Laura Lima - 27/03/2022
    Trabalho 2 de Sistemas Operacionais - Algoritmos de substituição de paginas """

def _ler_arquivo(caminho_arquivo):
    """
    Esta função recebe como parametro o caminho do arquivo que precisa ser lido.
    """
    ref_arquivo = open(caminho_arquivo,"r")

    return ref_arquivo.read().replace("\n","").split(";")

""" Substituição de página pelo algoritmo FIFO 
    Nessa implementação, todas as páginas são alocadas numa fila que representa a RAM
    Sendo assim, o primeiro elemento da fila é a página mais antiga
    A página no inicio da fila é substituida quando uma nova página precisa ser alocada
"""
def _page_faults_by_fifo(pages, number_pages, capacity):
    page_table = set() # Set que representa a page table (tabela que guarda a referencia das page frames NÃO vazias no momento)
    ram = [] # Vetor que vai representar a RAM (page frames)
  
    page_faults = 0
    for i in range(number_pages):
        # Primeiro, checar se a RAM ainda tem alguma page frame livre para alocar a pagina
        if (len(ram) < capacity):
              
            # Caso a página acessada ainda não existe na RAM, ela vai ser inserida
            if (pages[i] not in ram):
                # Atualiza a page table
                page_table.add(pages[i]) 

                # Aloca a página na RAM (fila)
                ram.append(pages[i])

                # Incrementa page faults
                page_faults += 1               
  
        # Caso não existe page frame disponivel
        # faz-se a remoção do primeiro elemento da fila (o mais antigo) de ambos a RAM e da page table
        # E por fim insere a página que esta sendo acessada (na RAM e na page table)
        else:              
            # Caso página NÃO existe na page table
            if (pages[i] not in page_table):                  
                # Remove a pagina mais antiga (primeiro elemento da fila)
                val = ram.pop(0) 
  
                # Atualiza a page table (remove a referencia da pagina que foi removida e insere a referencia para a nova pagina)
                page_table.remove(val)
                page_table.add(pages[i]) 
  
                # Aloca a nova página na RAM
                ram.append(pages[i]) 
  
                # Incrementa page_fault
                page_faults += 1

    return page_faults

""" Substituição de página pelo algoritmo LRU (Last recently used)
    Nessa implementação, quando a RAM não tem mais page frames livres, a página mais antiga é removida e então a nova é alocada no seu lugar
    Caso é acessado uma página que ja existe na RAM, a mesma é realocada para o final da fila (RAM)
"""
def _page_faults_by_LRU(pages, capacity):
    ram = [] # Vetor que vai representar a RAM (page frames)
    page_faults = 0 
    for i in pages: 
        # Caso pagina ainda não alocada na RAM, ela precisa ser adicionada
        if i not in ram:    
            # Caso não exista nenhuma page frame livre, então retira-se a página mais antiga (no caso, o primeiro elemento da fila)
            # e então a nova página é alocada
            if(len(ram) == capacity):
                ram.pop(0)
                ram.append(i)    
            # Caso ainda exista page frames disponpiveis naa RAM, a nova página é simplesmente alocada no fim
            else:
                ram.append(i)    
            page_faults +=1
        # Caso a página já existe na RAM, ela é removida e adicionada novamente na ultima posição da fila
        else:            
            ram.remove(i)    
            ram.append(i)

    return page_faults

# Função auxiliar que vai servir para marcar qual página está recebendo uma segunda chance
def _find_and_update(current_page, ram, second_chance_array, frames):     
    for i in range(frames):           
        if ram[i] == current_page:
            # Se página já está na RAM, recebe uma segunda chance
            second_chance_array[i] = 1            
            return True # Significa que foi acessado uma página que ja existe e não é preciso substituir nenhuma page frame   
    return False # Signica que a página que esta sendo acessada ainda não existe na RAM 
   
# Função que vai atualizar a página que já está em RAM e retornar um ponteiro
def _replace_and_update(page, ram, second_chance, frames, pointer):
    while(True):       
        if not second_chance[pointer]: # Caso não é a segunda chance daquela página apontada para ser removida             
            ram[pointer] = page # Aloca no page frame apontado a nova página
            return (pointer + 1) % frames # Retorna o ponteiro atualizado 
           
        # Marca-se a page frame com False 
        # Significa que aquela pagina vai ser substituida no proximo ciclo, a não ser que seja acessada novamente
        second_chance[pointer] = 0           
        pointer = (pointer + 1) % frames # Atualiza o ponteiro 


def _page_faults_by_SC(reference_string, number_pages, frames):
    pointer = 0 # Posição na RAM que referencia a pagina a ser removida
    page_faults = 0
    ram = [-1]*frames # Vetor que representa a RAM (page frames) preenchido com -1 que significa que páginas ainda não foram alocadas
    second_chance_array = [0]*frames # Vetor que vai servir para controlar a chance atual de cada page frame na RAM ( 0 -> False, 1 -> True)
              
    for i in range(number_pages):
        current_page = reference_string[i]           
        # Primeiro, a função auxiliar verifica que a página atual já existe na RAM
        if not _find_and_update(current_page,ram,second_chance_array,frames):
            # Caso não, a página atual é inserida       
            # Para isso, a função auxiliar _replace_and_update vai encontrar uma página para ser removida 
            pointer = _replace_and_update(current_page,ram,second_chance_array,frames,pointer)
            page_faults += 1
       
    return page_faults

caminho_arquivo = input(f"Insira o caminho do arquivo: ")
pages_references = _ler_arquivo(caminho_arquivo)[:-2] # Vetor com todos as referencias do arquivo (excluindo a referencia 0,0 que indica fim da string)
SIZE_PAGES_SLOT = 8000 # Constante para definir o tamanho do vetor que representa uma memória de 32MB

page_faults_FIFO = _page_faults_by_fifo(pages_references, len(pages_references), SIZE_PAGES_SLOT)
page_faults_by_LRU = _page_faults_by_LRU(pages_references, SIZE_PAGES_SLOT)
page_faults_by_SC = _page_faults_by_SC(pages_references, len(pages_references), SIZE_PAGES_SLOT)
print("FIFO -", page_faults_FIFO)
print("LRU -", page_faults_by_LRU)
print("Segunda Chance -", page_faults_by_SC)