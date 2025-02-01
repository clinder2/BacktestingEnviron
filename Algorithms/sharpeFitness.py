import numpy as np

def fitness(weights, prices):
    p_returns = np.log(prices) - np.log(prices.shift(1))
    p_returns = p_returns.dropna()
    portfolio_returns = np.dot(p_returns, weights)
    portfolio_mean = np.mean(portfolio_returns)
    portfolio_std = np.std(portfolio_returns)
    sharpe_ratio = portfolio_mean/portfolio_std
    #print(str(sharpe_ratio) + ", " + str(weights))
    return sharpe_ratio