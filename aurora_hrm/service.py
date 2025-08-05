'''
Reasoning Service Module
========================

Serviço assíncrono para operações de raciocínio usando HRM.
'''

import asyncio
import threading
from typing import Dict, Any, Optional
import logging
from .wrapper import HRMWrapper

logger = logging.getLogger(__name__)


class ReasoningService:
    '''Serviço de raciocínio assíncrono para o Aurora'''
    
    def __init__(self):
        '''Inicializa o serviço de raciocínio'''
        self.hrm = HRMWrapper()
        self.is_initialized = False
        self._lock = threading.Lock()
        self._executor = None
        
        logger.info('ReasoningService criado')
    
    async def initialize(self, model_path: Optional[str] = None) -> bool:
        '''
        Inicializa o serviço de raciocínio.
        
        Args:
            model_path: Caminho para o modelo (opcional)
            
        Returns:
            bool: True se inicializado com sucesso
        '''
        loop = asyncio.get_event_loop()
        
        def _initialize():
            with self._lock:
                if model_path:
                    success = self.hrm.load_model(model_path)
                else:
                    # Inicialização sem modelo específico
                    success = True
                    self.hrm.is_loaded = True
                
                self.is_initialized = success
                return success
        
        try:
            result = await loop.run_in_executor(None, _initialize)
            logger.info(f'Serviço inicializado: {result}')
            return result
        except Exception as e:
            logger.error(f'Erro ao inicializar serviço: {e}')
            return False
    
    async def solve_puzzle(self, puzzle_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Resolve puzzle usando HRM de forma assíncrona.
        
        Args:
            puzzle_type: Tipo do puzzle ('sudoku', 'maze')
            data: Dados do puzzle
            
        Returns:
            Dict com resultado da resolução
        '''
        if not self.is_initialized:
            return {'error': 'Serviço não inicializado'}
        
        loop = asyncio.get_event_loop()
        
        def _solve():
            try:
                if puzzle_type.lower() == 'sudoku':
                    return self.hrm.solve_sudoku(data.get('puzzle', []))
                elif puzzle_type.lower() == 'maze':
                    return self.hrm.solve_maze(
                        data.get('maze', []),
                        data.get('start', (0, 0)),
                        data.get('end', (0, 0))
                    )
                else:
                    return {'error': f'Tipo de puzzle não suportado: {puzzle_type}'}
            except Exception as e:
                logger.error(f'Erro na resolução: {e}')
                return {'error': str(e)}
        
        try:
            result = await loop.run_in_executor(None, _solve)
            logger.info(f'Puzzle {puzzle_type} resolvido: {result.get(\
success\, False)}')
            return result
        except Exception as e:
            logger.error(f'Erro assíncrono: {e}')
            return {'error': str(e)}
    
    async def solve_sudoku_async(self, puzzle: list) -> Dict[str, Any]:
        '''Resolve Sudoku de forma assíncrona'''
        return await self.solve_puzzle('sudoku', {'puzzle': puzzle})
    
    async def solve_maze_async(self, maze: list, start: tuple, end: tuple) -> Dict[str, Any]:
        '''Resolve labirinto de forma assíncrona'''
        return await self.solve_puzzle('maze', {
            'maze': maze,
            'start': start,
            'end': end
        })
    
    def get_status(self) -> Dict[str, Any]:
        '''Retorna status do serviço'''
        return {
            'initialized': self.is_initialized,
            'model_loaded': self.hrm.is_loaded if hasattr(self.hrm, 'is_loaded') else False,
            'device': str(self.hrm.device) if hasattr(self.hrm, 'device') else 'unknown',
            'capabilities': ['sudoku', 'maze'] if self.is_initialized else []
        }
    
    async def shutdown(self):
        '''Finaliza o serviço'''
        logger.info('Finalizando ReasoningService...')
        self.is_initialized = False
        if self._executor:
            self._executor.shutdown(wait=True)

