'''
Exemplo de uso - Resolução de Sudoku
=====================================

Este exemplo demonstra como usar o Aurora HRM Wrapper para resolver puzzles Sudoku.
'''

import asyncio
import sys
import os

# Adicionar o diretório pai ao path para importar aurora_hrm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora_hrm import ReasoningService


async def main():
    '''Função principal do exemplo'''
    print('🧩 Aurora HRM Wrapper - Exemplo Sudoku')
    print('=' * 40)
    
    # Inicializar serviço
    reasoning = ReasoningService()
    print('Inicializando serviço de raciocínio...')
    
    success = await reasoning.initialize()
    if not success:
        print('❌ Erro ao inicializar serviço')
        return
    
    print('✅ Serviço inicializado com sucesso')
    
    # Puzzle Sudoku de exemplo (0 = célula vazia)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    print('\\nPuzzle original:')
    print_sudoku(puzzle)
    
    # Resolver puzzle
    print('\\n🤔 Resolvendo puzzle...')
    result = await reasoning.solve_puzzle('sudoku', {'puzzle': puzzle})
    
    if result.get('success'):
        print('✅ Puzzle resolvido com sucesso!')
        print(f'📊 Confiança: {result.get(\
confidence\, 0):.2%}')
        print(f'🔢 Passos: {result.get(\steps\, \N/A\)}')
        print('\\nSolução:')
        print_sudoku(result['solution'])
    else:
        print(f'❌ Erro ao resolver: {result.get(\error\, \Erro
desconhecido\)}')
    
    # Status do serviço
    status = reasoning.get_status()
    print('\\n📋 Status do serviço:')
    for key, value in status.items():
        print(f'  {key}: {value}')


def print_sudoku(grid):
    '''Imprime o grid do Sudoku de forma formatada'''
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print('------+-------+------')
        
        row_str = ''
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += '| '
            
            if cell == 0:
                row_str += '. '
            else:
                row_str += f'{cell} '
        
        print(row_str)


if __name__ == '__main__':
    asyncio.run(main())

