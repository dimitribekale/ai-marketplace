# AI Marketplace

A decentralized marketplace for buying and selling AI models and datasets using smart contracts. This project leverages blockchain technology to create a trustless, peer-to-peer marketplace without intermediaries taking a cut.

## Project Overview

This marketplace uses Solidity smart contracts as an automated escrow agent, enabling:

- **Trustless Transactions**: Buy and sell AI models without a central authority
- **Smart Contract Escrow**: Automated payment handling and model delivery
- **Decentralized Architecture**: No middleman fees or central point of control
- **Event-Driven Notifications**: Real-time updates on purchases and listings

Built with Hardhat 3, TypeScript, and Viem for modern Ethereum development.

## Usage

### Running Tests

To run all the tests in the project, execute the following command:

```shell
npx hardhat test
```

You can also selectively run the Solidity or `node:test` tests:

```shell
npx hardhat test solidity
npx hardhat test nodejs
```

### Make a deployment to Sepolia

This project includes an example Ignition module to deploy the contract. You can deploy this module to a locally simulated chain or to Sepolia.

To run the deployment to a local chain:

```shell
npx hardhat ignition deploy ignition/modules/Counter.ts
```

To run the deployment to Sepolia, you need an account with funds to send the transaction. The provided Hardhat configuration includes a Configuration Variable called `SEPOLIA_PRIVATE_KEY`, which you can use to set the private key of the account you want to use.

You can set the `SEPOLIA_PRIVATE_KEY` variable using the `hardhat-keystore` plugin or by setting it as an environment variable.

To set the `SEPOLIA_PRIVATE_KEY` config variable using `hardhat-keystore`:

```shell
npx hardhat keystore set SEPOLIA_PRIVATE_KEY
```

After setting the variable, you can run the deployment with the Sepolia network:

```shell
npx hardhat ignition deploy --network sepolia ignition/modules/Counter.ts
```
