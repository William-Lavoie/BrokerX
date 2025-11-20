from uuid import UUID

from portfolio.adapters.dao.mysql_portfolio_dao import MySQLPortfolioDAO
from portfolio.domain.ports.portfolio_repository import PortfolioRepository
from portfolio.models import Portfolio
from portfolio.domain.entities.portfolio import PortfolioInvalidException

class DjangoWalletRepository(PortfolioRepository):
    def __init__(self, dao=None, redis=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLPortfolioDAO()
       # self.redis = redis if redis is not None else RedisPortfolio()

    def get_portfolio(self, client_id: UUID) -> Portfolio:
        portfolio_dto = self.dao.get_portfolio(client_id=client_id)
        if not portfolio_dto.success:
            raise PortfolioInvalidException()
        
       # self.redis.set_wallet_balance(
        #    client_id=client_id, balance=wallet_dto.balance
        #)

        return self.get_portfolio_from_dto(portfolio_dto)