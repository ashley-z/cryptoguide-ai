# Compound III Documentation

## Introduction

Compound III is an EVM compatible protocol that enables supplying of crypto assets as collateral in order to borrow the base asset. Accounts can also earn interest by supplying the base asset to the protocol. The initial deployment of Compound III is on Ethereum and the base asset is USDC.

## Interest Rates

Users with a positive balance of the base asset earn interest, denominated in the base asset, based on a supply rate model; users with a negative balance pay interest based on a borrow rate model. These are separate interest rate models, and set by governance.

The supply and borrow interest rates are a function of the utilization rate of the base asset. Each model includes a utilization rate "kink" - above this point the interest rate increases more rapidly. Interest accrues every second using the block timestamp.

Collateral assets do not earn or pay interest.

## Collateral & Borrowing

Users can add collateral assets to their account using the supply function. Collateral can only be added if the market is below its supplyCap, which limits the protocol's risk exposure to collateral assets.

Each collateral asset increases the user's borrowing capacity, based on the asset's borrowCollateralFactor. The borrowing collateral factors are percentages that represent the portion of collateral value that can be borrowed.

For instance, if the borrow collateral factor for WBTC is 85%, an account can borrow up to 85% of the USD value of its supplied WBTC in the base asset. Collateral factors can be fetched using the Get Asset Info By Address function.

The base asset can be borrowed using the withdraw function; the resulting borrow balance must meet the borrowing collateral factor requirements. If a borrowing account subsequently fails to meet the borrow collateral factor requirements, it cannot borrow additional assets until it supplies more collateral, or reduces its borrow balance using the supply function.

Account balances for the base token are signed integers. An account balance greater than zero indicates the base asset is supplied and a balance less than zero indicates the base asset is borrowed.

Account balances are stored internally in Comet as principal values (also signed integers). The principal value, also referred to as the day-zero balance, is what an account balance at T0 would have to be for it to be equal to the account balance today after accruing interest.

Global indices for supply and borrow are unsigned integers that increase over time to account for the interest accrued on each side.

Balance = Principal * BaseSupplyIndex [Principal > 0]
Balance = Principal * BaseBorrowIndex [Principal < 0]

### Borrow Collateralization

The isBorrowCollateralized function returns true if the account has non-negative liquidity based on the borrow collateral factors. A return value of false does not necessarily imply that the account is presently liquidatable (see isLiquidatable function).

### Minimum Borrow Balance

The baseBorrowMin function returns the minimum borrow balance allowed in the base asset. An account's initial borrow size must be equal to or greater than this value.

## Liquidation

Liquidation is determined by liquidation collateral factors, which are separate and higher than borrow collateral factors (used to determine initial borrowing capacity), which protects borrowers & the protocol by ensuring a price buffer for all new positions. These also enable governance to reduce borrow collateral factors without triggering the liquidation of existing positions.

When an account's borrow balance exceeds the limits set by liquidation collateral factors, it is eligible for liquidation. A liquidator (a bot, contract, or user) can call the absorb function, which relinquishes ownership of the accounts collateral, and returns the value of the collateral, minus a penalty (liquidationFactor), to the user in the base asset. The liquidated user has no remaining debt, and typically, will have an excess (interest earning) balance of the base asset.

Each absorption is paid for by the protocol's reserves of the base asset. In return, the protocol receives the collateral assets. If the remaining reserves are less than a governance-set target, liquidators are able to buy the collateral at a discount using the base asset, which increases the protocol's base asset reserves.

### Liquidatable Accounts

The isLiquidatable function returns true if the account has negative liquidity based on the liquidation collateral factor. A return value of true indicates that the account is presently liquidatable.

### Absorb

The absorb function can be called by any address to liquidate an underwater account. It transfers the account's debt to the protocol account, decreases cash reserves to repay the account's borrows, and adds the collateral to the protocol's own balance. The caller has the amount of gas spent noted.

### Buy Collateral

This function allows any account to buy collateral from the protocol, at a discount from the Price Feed's price, using base tokens. A minimum collateral amount should be specified to indicate the maximum slippage acceptable for the buyer.

## Governance

Compound III is a decentralized protocol that is governed by holders and delegates of COMP. Governance allows the community to propose, vote, and implement changes through the administrative smart contract functions of the Compound III protocol.

All instances of Compound III are controlled by the Timelock contract which is the same administrator of the Compound v2 protocol. The governance system has control over each proxy, the Configurator implementation, the Comet factory, and the Comet implementation.

Each time an immutable parameter is set via governance proposal, a new Comet implementation must be deployed by the Comet factory. If the proposal is approved by the community, the proxy will point to the new implementation upon execution.

## Protocol Rewards

Compound III has a built-in system for tracking rewards for accounts that use the protocol. The full history of accrual of rewards are tracked for suppliers and borrowers of the base asset. The rewards can be any ERC-20 token. In order for rewards to accrue to Compound III accounts, the configuration's baseMinForRewards threshold for total supply of the base asset must be met.
