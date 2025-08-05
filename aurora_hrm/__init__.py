'''
Aurora HRM Wrapper
==================

Wrapper inteligente para integrar o Hierarchical Reasoning Model (HRM) no projeto Aurora.

Exports principais:
- HRMWrapper: Classe wrapper principal para o modelo HRM
- ReasoningService: Serviço assíncrono para raciocínio
'''

from .wrapper import HRMWrapper
from .service import ReasoningService

__version__ = '1.0.0'
__author__ = 'Aurora AI Team'
__email__ = 'team@aurora-ai.com'

__all__ = [
    'HRMWrapper',
    'ReasoningService',
]
