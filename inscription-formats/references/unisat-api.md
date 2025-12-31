# UniSat API Reference

## Overview

UniSat 提供两套独立的 API 服务，分别用于 Bitcoin 主网和 Fractal 网络。

**官方资源：**
- Swagger UI: https://open-api.unisat.io
- GitHub Docs: https://github.com/unisat-wallet/unisat-dev-docs
- API Key 申请: https://developer.unisat.io

---

## 网络区分

| 网络 | Base URL | 特有功能 |
|------|----------|---------|
| **Bitcoin Mainnet** | `https://open-api.unisat.io` | Runes, Alkanes, 完整 Marketplace |
| **Bitcoin Testnet** | `https://open-api-testnet.unisat.io` | 测试环境 |
| **Fractal Mainnet** | `https://open-api-fractal.unisat.io` | BRC20-Swap, CAT20 DEX |
| **Fractal Testnet** | `https://open-api-fractal-testnet.unisat.io` | 测试环境 |

⚠️ **重要**：Bitcoin 主网和 Fractal 是完全独立的链，余额、铭文、交易互不相通。

---

## Authentication

```javascript
const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Content-Type': 'application/json'
};
```

---

# Part 1: Blockchain Indexing API（两网络通用）

## 1.1 Blockchain Level

### Get Blockchain Info
```
GET /v1/indexer/blockchain/info
```

### Get Block Info
```
GET /v1/indexer/block/{height}/info
```

### Get Recommended Fees
```
GET /v1/indexer/fee/recommend
```

**Response:**
```json
{
  "code": 0,
  "data": {
    "fastestFee": 50,
    "halfHourFee": 40,
    "hourFee": 30,
    "minimumFee": 10
  }
}
```

## 1.2 Address Endpoints

### Get Address Balance
```
GET /v1/indexer/address/{address}/balance
```

### Get Address UTXOs
```
GET /v1/indexer/address/{address}/utxo-data
```

**Response:**
```json
{
  "code": 0,
  "data": {
    "utxo": [
      {
        "txid": "abc123...",
        "vout": 0,
        "satoshi": 10000,
        "scriptType": "P2TR",
        "inscriptions": [],
        "runes": []
      }
    ]
  }
}
```

## 1.3 Inscription Indexer

### Get Inscription Info
```
GET /v1/indexer/inscription/info/{inscriptionId}
```

### Get Inscription Content
```
GET /v1/indexer/inscription/content/{inscriptionId}
```

### Get Address Inscriptions
```
GET /v1/indexer/address/{address}/inscription-data?cursor=0&size=16
```

### Search Inscriptions
```
GET /v1/indexer/inscription/search
```

## 1.4 BRC-20 Indexer

### Get BRC-20 Token Info
```
GET /v1/indexer/brc20/{ticker}/info
```

**Response:**
```json
{
  "code": 0,
  "data": {
    "ticker": "ordi",
    "holdersCount": 12345,
    "inscriptionId": "abc...i0",
    "max": "21000000",
    "limit": "1000",
    "minted": "21000000",
    "decimal": 18
  }
}
```

### Get Address BRC-20 Balance
```
GET /v1/indexer/address/{address}/brc20/summary
```

### Get Transferable Inscriptions
```
GET /v1/indexer/address/{address}/brc20/{ticker}/transferable-inscriptions
```

### Get BRC-20 History
```
GET /v1/indexer/brc20/{ticker}/history
```

Query params: `start`, `limit`, `type` (inscribe-mint, inscribe-transfer, transfer)

## 1.5 Transaction Endpoints

### Broadcast Transaction
```
POST /v1/indexer/tx/broadcast
```

**Request:**
```json
{ "rawtx": "0200000001..." }
```

### Get Transaction Info
```
GET /v1/indexer/tx/{txid}
```

---

# Part 2: Bitcoin 主网专有 API

Base URL: `https://open-api.unisat.io`

## 2.1 Runes Indexer

⚠️ **Bitcoin 主网专有**

### Get Runes Status
```
GET /v1/indexer/runes/status
```

### Get Rune Info
```
GET /v1/indexer/runes/info/{runeid}
```

Rune ID format: `{block}:{tx}` (e.g., `840000:1`)

### Get Address Runes Balance
```
GET /v1/indexer/address/{address}/runes/balance-list
```

### Get Rune Holders
```
GET /v1/indexer/runes/{runeid}/holders
```

### Get Rune UTXO
```
GET /v1/indexer/runes/{runeid}/utxo
```

## 2.2 Alkanes Indexer

⚠️ **Bitcoin 主网专有** - 2025年6月新增

### Get Alkanes Status
```
GET /v1/indexer/alkanes/status
```

### Get Alkanes List
```
GET /v1/indexer/alkanes/list?start=0&limit=10
```

### Search Alkanes
```
GET /v1/indexer/alkanes/search?keyword={keyword}
```

### Get Address Alkanes Balance
```
GET /v1/indexer/address/{address}/alkanes/balance-list
```

## 2.3 Collection Indexer

### Get Collections Stats
```
GET /v1/indexer/collection/stats
```

### Get Collections List
```
GET /v1/indexer/collection/list
```

### Search Collections
```
GET /v1/indexer/collection/search?keyword={keyword}
```

### Get Trending Collections
```
GET /v1/indexer/collection/trending
```

---

# Part 3: UniSat Services API

## 3.1 Inscribe API (铭刻服务)

用于创建铭文订单，无需自己维护 indexer。

### Create Order (通用)
```
POST /v2/inscribe/order/create
```

**Request:**
```json
{
  "receiveAddress": "bc1p...",
  "feeRate": 10,
  "outputValue": 546,
  "files": [
    {
      "filename": "test.txt",
      "dataURL": "data:text/plain;charset=utf-8;base64,SGVsbG8="
    }
  ],
  "devAddress": "bc1p...",
  "devFee": 0
}
```

### Create BRC-20 Deploy Order
```
POST /v2/inscribe/order/create/brc20-deploy
```

**Request:**
```json
{
  "receiveAddress": "bc1p...",
  "feeRate": 10,
  "outputValue": 546,
  "devAddress": "",
  "devFee": 0,
  "brc20Ticker": "TEST",
  "brc20Max": "21000000",
  "brc20Limit": "1000"
}
```

### Create BRC-20 Mint Order
```
POST /v2/inscribe/order/create/brc20-mint
```

**Request:**
```json
{
  "receiveAddress": "bc1p...",
  "feeRate": 10,
  "outputValue": 546,
  "brc20Ticker": "TEST",
  "brc20Amount": "1000"
}
```

### Create BRC-20 Transfer Order
```
POST /v2/inscribe/order/create/brc20-transfer
```

**Request:**
```json
{
  "receiveAddress": "bc1p...",
  "feeRate": 10,
  "outputValue": 546,
  "brc20Ticker": "TEST",
  "brc20Amount": "100"
}
```

### Search Order
```
GET /v2/inscribe/order/{orderId}
```

建议每 10 秒查询一次订单状态。

**Response:**
```json
{
  "code": 0,
  "data": {
    "orderId": "...",
    "status": "pending|paid|inscribing|completed|failed",
    "payAddress": "bc1p...",
    "amount": 10000,
    "minerFee": 5000,
    "serviceFee": 1000,
    "devFee": 0
  }
}
```

费用计算: `amount = outputValue * count + minerFee + serviceFee + devFee`

### Get Order List
```
GET /v2/inscribe/order/list?cursor=0&size=10
```

### Refund Estimate
```
POST /v2/inscribe/order/{orderId}/refund-estimate
```

### Refund
```
POST /v2/inscribe/order/{orderId}/refund
```

## 3.2 BRC-20 Marketplace API

⚠️ API 版本为 v3

### Get Market Statistics
```
POST /v3/market/brc20/auction/brc20_types
```

**Request:**
```json
{
  "timeType": "day1",  // day1, day7, day30
  "ticks": ["ordi", "sats"],
  "start": 0,
  "limit": 10
}
```

### Get K-Line Data
```
POST /v3/market/brc20/auction/brc20_kline
```

**Request:**
```json
{
  "tick": "ordi",
  "timeStart": 1700000000000,
  "timeEnd": 1700100000000,
  "timeStep": 300000
}
```

限制: `(timeEnd - timeStart) / timeStep <= 2016`

### Get Market Listings
```
POST /v3/market/brc20/auction/list
```

**Request:**
```json
{
  "filter": {
    "nftType": "brc20",
    "tick": "ordi",
    "minPrice": 1,
    "maxPrice": 100000
  },
  "sort": {
    "unitPrice": 1
  },
  "start": 0,
  "limit": 20
}
```

### Create Listing (上架)
```
POST /v3/market/brc20/auction/create_put_on
```

**Request:**
```json
{
  "nftType": "brc20",
  "inscriptionId": "abc123...i0",
  "initPrice": "10000",
  "unitPrice": "100",
  "pubkey": "02...",
  "marketType": "fixedPrice"
}
```

### Confirm Listing
```
POST /v3/market/brc20/auction/confirm_put_on
```

**Request:**
```json
{
  "auctionId": "...",
  "psbt": "...",
  "fromBase64": true
}
```

### Create Purchase (购买)
```
POST /v3/market/brc20/auction/create_bid
```

### Confirm Purchase
```
POST /v3/market/brc20/auction/confirm_bid
```

### Create Delist (下架)
```
POST /v3/market/brc20/auction/create_put_off
```

### Confirm Delist
```
POST /v3/market/brc20/auction/confirm_put_off
```

## 3.3 Runes Marketplace API

与 BRC-20 Marketplace 类似，Base path: `/v3/market/runes/auction/`

## 3.4 Alkanes Marketplace API

与 BRC-20 Marketplace 类似，Base path: `/v3/market/alkanes/auction/`

## 3.5 Collection Marketplace API

NFT 集合交易，Base path: `/v3/market/collection/auction/`

## 3.6 Domain Marketplace API

域名交易（.sats 等），Base path: `/v3/market/domain/auction/`

---

# Part 4: Fractal 网络 API

Base URL: `https://open-api-fractal.unisat.io`
Testnet: `https://open-api-fractal-testnet.unisat.io`

⚠️ **重要修正**：Fractal 网络**也支持 Runes**！之前说"Fractal 不支持 Runes"是错误的。

---

## 4.1 Fractal Indexer API（与 Bitcoin 结构相同）

Fractal 的 Indexer API 与 Bitcoin 主网结构完全相同，只是 Base URL 不同。

### General - Blocks
```
GET /v1/indexer/blockchain/info
GET /v1/indexer/block/{height}/txs
```

### General - Transactions
```
GET /v1/indexer/tx/{txid}
GET /v1/indexer/tx/{txid}/ins
GET /v1/indexer/tx/{txid}/outs
GET /v1/indexer/utxo/{txid}/{index}
```

### General - Addresses
```
GET /v1/indexer/address/{address}/balance
GET /v1/indexer/address/{address}/history
GET /v1/indexer/address/{address}/utxo
GET /v1/indexer/address/{address}/inscription-utxo
```

### Inscriptions
```
GET /v1/indexer/inscription/info/{inscriptionId}
GET /v1/indexer/inscription/content/{inscriptionId}
GET /v1/indexer/inscription/{inscriptionId}/events
GET /v1/indexer/address/{address}/inscription-data
```

### BRC-20 Indexer
```
GET /v1/indexer/brc20/bestheight
GET /v1/indexer/brc20/list
GET /v1/indexer/brc20/status
GET /v1/indexer/brc20/{ticker}/info
GET /v1/indexer/brc20/{ticker}/holders
GET /v1/indexer/brc20/{ticker}/history
GET /v1/indexer/brc20/{ticker}/history-by-height
GET /v1/indexer/brc20/{ticker}/tx-history
GET /v1/indexer/address/{address}/brc20/summary
GET /v1/indexer/address/{address}/brc20/{ticker}/info
GET /v1/indexer/address/{address}/brc20/{ticker}/history
```

### Runes Indexer（Fractal 也支持！）
```
GET /v1/indexer/runes/status
GET /v1/indexer/runes/info-list
GET /v1/indexer/runes/info/{runeid}
GET /v1/indexer/runes/{runeid}/holders
GET /v1/indexer/address/{address}/runes/balance-list
GET /v1/indexer/address/{address}/runes/{runeid}/balance
GET /v1/indexer/utxo/{txid}/{index}/runes/balance
GET /v1/indexer/address/{address}/runes/{runeid}/utxo
GET /v1/indexer/runes/{runeid}/events
```

---

## 4.2 Fractal 链统计 API

### Get Circulating Supply
```
GET /v1/public/fractal/supply
```

添加 `?format=text` 返回带 FB 单位的文本格式。

### Get Total Supply
```
GET /v1/public/fractal/total-supply
```

### Get Total Address Count
```
GET /v1/public/fractal/address-count
```

### Get Rich Address List
```
GET /v1/public/fractal/rich-list
```

---

## 4.3 UniSat Inscribe on Fractal

与 Bitcoin 主网的 Inscribe API 相同，Base URL 换成 Fractal。

```
GET  /v2/inscribe/order/summary
GET  /v2/inscribe/order/list
POST /v2/inscribe/order/create
GET  /v2/inscribe/order/{orderId}
POST /v2/inscribe/order/{orderId}/refund-estimate
POST /v2/inscribe/order/{orderId}/refund
POST /v2/inscribe/order/create/brc20-deploy
POST /v2/inscribe/order/create/brc20-mint
POST /v2/inscribe/order/create/brc20-transfer
```

---

## 4.4 UniSat Marketplace on Fractal

Fractal 上的 Marketplace API 与 Bitcoin 主网结构相同：

```
/v3/market/brc20/auction/...    # BRC-20 Marketplace
/v3/market/runes/auction/...    # Runes Marketplace
/v3/market/collection/auction/... # Collection Marketplace
/v3/market/domain/auction/...   # Domain Marketplace
```

### Collection Marketplace 示例
```javascript
// 获取 Collection 统计
const response = await fetch('https://open-api-fractal.unisat.io/v3/market/collection/auction/collection_statistic', {
  method: 'POST',
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ "collectionId": "your-collection-id" })
});

// Response
{
  "code": 0,
  "data": {
    "collectionId": "...",
    "name": "...",
    "floorPrice": 100000,
    "listed": 50,
    "total": 1000,
    "supply": 1000
  }
}
```

---

## 4.5 UniSat Collection on Fractal

Fractal 专属的 Collection 管理 API：

```
GET  /v1/indexer/collection/status
GET  /v1/indexer/collection/list
GET  /v1/indexer/collection/{collectionId}/info
GET  /v1/indexer/collection/{collectionId}/holders
GET  /v1/indexer/address/{address}/collection/list
GET  /v1/indexer/collection/{collectionId}/items
GET  /v1/indexer/address/{address}/collection/summary
GET  /v1/indexer/address/{address}/collection/{collectionId}/items
GET  /v1/indexer/inscription/{inscriptionId}/collection
POST /v1/indexer/collection/{collectionId}/items/add
POST /v1/indexer/collection/{collectionId}/items/remove
```

---

## 4.6 PizzaSwap / BRC20-Swap API

⚠️ **Fractal 专有功能**：链下转账，无需 BTC 矿工费，使用 BRC-20 代币作为手续费。

### 转账流程（三步）

```
1. pre_send  →  获取签名消息和费用信息
2. sign      →  用钱包私钥对消息签名 (bip322-simple)
3. send      →  提交签名完成转账
```

### Step 1: Pre-Send
```
GET /v1/brc20-swap/pre_send
```

**Query Parameters:**

| Field | Type | Description |
|-------|------|-------------|
| address | string | 发送者地址 |
| tick | string | 要发送的 tick |
| amount | string | 发送数量 |
| to | string | 接收者地址 |
| ts | number | 时间戳（秒级） |
| feeTick | string | 手续费 tick |
| payType | string | 固定 `"brc20"` |

**Response:**
```json
{
  "code": 0,
  "data": {
    "ids": ["..."],
    "signMsgs": ["message1", "message2"],
    "feeAmount": "100",
    "feeTickPrice": "0.001",
    "feeBalance": "10000"
  }
}
```

### Step 2: Sign Messages

```typescript
import { AddressType, wallet } from "@unisat/wallet-sdk";
import { NetworkType } from "@unisat/wallet-sdk/lib/network/index.js";

async function signMessages(signMsgs: string[], wifKey: string): Promise<string[]> {
  const walletInstance = new wallet.LocalWallet(
    wifKey, 
    AddressType.P2TR, 
    NetworkType.MAINNET  // Fractal 也用 MAINNET
  );
  
  const signatures: string[] = [];
  for (const msg of signMsgs) {
    const sig = await walletInstance.signMessage(msg, 'bip322-simple');
    signatures.push(sig);
  }
  return signatures;
}
```

### Step 3: Send
```
POST /v1/brc20-swap/send
```

**Request:**
```json
{
  "address": "bc1p...",
  "tick": "ordi",
  "amount": "100",
  "to": "bc1p...",
  "ts": 1700000000,
  "feeTick": "sFB___000",
  "feeAmount": "100",
  "feeTickPrice": "0.001",
  "payType": "brc20",
  "sigs": ["sig1", "sig2"]
}
```

### 完整转账示例

```typescript
import { AddressType, wallet } from "@unisat/wallet-sdk";
import { NetworkType } from "@unisat/wallet-sdk/lib/network/index.js";
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://open-api-fractal.unisat.io',
  headers: { 'Authorization': `Bearer ${API_KEY}` }
});

async function transferBRC20OnFractal(
  from: string,
  to: string,
  tick: string,
  amount: string,
  feeTick: string,
  wifKey: string
) {
  const ts = Math.floor(Date.now() / 1000);
  
  // 1. Pre-send
  const { data: preData } = await api.get('/v1/brc20-swap/pre_send', {
    params: { address: from, tick, amount, to, ts, feeTick, payType: 'brc20' }
  });
  if (preData.code !== 0) throw new Error(preData.msg);
  
  await new Promise(r => setTimeout(r, 1000));
  
  // 2. Sign
  const walletInstance = new wallet.LocalWallet(wifKey, AddressType.P2TR, NetworkType.MAINNET);
  const sigs: string[] = [];
  for (const msg of preData.data.signMsgs) {
    sigs.push(await walletInstance.signMessage(msg, 'bip322-simple'));
  }
  
  // 3. Send
  const { data: sendData } = await api.post('/v1/brc20-swap/send', {
    address: from, tick, amount, to, ts, feeTick,
    feeAmount: preData.data.feeAmount,
    feeTickPrice: preData.data.feeTickPrice,
    payType: 'brc20',
    sigs
  });
  
  if (sendData.code !== 0) throw new Error(sendData.msg);
  return sendData.data.id;
}
```

### 批量转账注意事项

- 每次转账间隔 **3-10 秒**
- `ts` 使用 **秒级** 时间戳
- 签名必须用 `bip322-simple`
- `feeAmount`/`feeTickPrice` 必须原样传回

### Fractal 常见费用 Tick

| Tick | 说明 |
|------|------|
| `sFB___000` | Fractal 常用费用代币 |

---

## 4.7 CAT Market API

⚠️ **独立的 API 服务**

CAT Market 有独立的 API 文档站点：
- Swagger UI: https://api.catmarket.io/api-docs/

需要增加 API 限流可联系 UniSat Discord。

---

## 4.8 CAT20-DEX API

⚠️ **Fractal 专有** - CAT20 去中心化交易

### Get Token Price
```
GET /v1/cat20-dex/getTokenPrice?tokenId={tokenId}
```

**示例 tokenId:** `45ee725c2c5993b3e4d308842d87e973bf1951f5f7a804b21e4dd964ecd12d6b_0`

**Response:**
```json
{
  "code": 1,
  "msg": "OK",
  "data": {
    "askPrice": 197000,
    "bidPrice": 195000,
    "latestTradePrice": 196000,
    "timestamp": "2024-01-01T00:00:00Z",
    "height": 123456
  }
}
```

**价格说明:**
- 价格单位是 satoshis / 0.01 CAT
- `askPrice: 197000` = 197000 sats / 0.01 CAT = **0.197 FB/CAT**
- `askPrice` = 卖方最低报价
- `bidPrice` = 买方最高出价

### Get Market Stats
```
GET /v1/cat20-dex/getMarketStats
```

**Query Parameters:**

| Field | Type | Description |
|-------|------|-------------|
| sortField | enum | volume, volume30d, volume7d, volume24h, volume6h |
| tokenId | string | 可选，指定 token |
| offset | int | 分页偏移 |
| limit | int | 数量限制（默认 20，最大 100） |

**Response:**
```json
{
  "code": 1,
  "msg": "OK",
  "data": {
    "tokenStats": {
      "tokenId": "...",
      "volume": "7169599786237",
      "volume30d": "...",
      "volume24h": "...",
      "volume7d": "...",
      "volume6h": "...",
      "price": 198000,
      "price6h": 195000,
      "price24h": 190000,
      "price7d": 180000,
      "price30d": 150000,
      "name": "CAT",
      "symbol": "CAT",
      "decimals": 2,
      "max": 21000000
    },
    "total": 50
  }
}
```

**成交量说明:**
- `volume` 单位是 satoshis
- `volume: 7169599786237` = **71695.99786237 FB**

---

# Part 5: SDK 封装示例

```typescript
type Network = 'bitcoin' | 'bitcoin-testnet' | 'fractal' | 'fractal-testnet';

const BASE_URLS: Record<Network, string> = {
  'bitcoin': 'https://open-api.unisat.io',
  'bitcoin-testnet': 'https://open-api-testnet.unisat.io',
  'fractal': 'https://open-api-fractal.unisat.io',
  'fractal-testnet': 'https://open-api-fractal-testnet.unisat.io'
};

class UniSatAPI {
  private baseUrl: string;
  private apiKey: string;
  private network: Network;

  constructor(apiKey: string, network: Network = 'bitcoin') {
    this.apiKey = apiKey;
    this.network = network;
    this.baseUrl = BASE_URLS[network];
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
    const data = await response.json();
    if (data.code !== 0) throw new Error(data.msg || 'API Error');
    return data.data;
  }

  // 通用
  async getBRC20Info(ticker: string) {
    return this.request(`/v1/indexer/brc20/${ticker}/info`);
  }

  async getAddressBalance(address: string) {
    return this.request(`/v1/indexer/address/${address}/balance`);
  }

  async getRecommendedFees() {
    return this.request('/v1/indexer/fee/recommend');
  }

  // Bitcoin 主网专用
  async getRuneInfo(runeid: string) {
    if (this.network.includes('fractal')) {
      throw new Error('Runes API only available on Bitcoin mainnet');
    }
    return this.request(`/v1/indexer/runes/info/${runeid}`);
  }

  async getAlkanesStatus() {
    if (this.network.includes('fractal')) {
      throw new Error('Alkanes API only available on Bitcoin mainnet');
    }
    return this.request('/v1/indexer/alkanes/status');
  }

  // 工具方法
  isFractal(): boolean {
    return this.network.includes('fractal');
  }
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| -1 | Unknown error |
| 10001 | Invalid parameter |
| 10002 | Rate limit exceeded |
| 10003 | Unauthorized |
| 10004 | Resource not found |

---

## API 分类速查表

### Bitcoin 主网 (`https://open-api.unisat.io`)

| 类别 | 路径前缀 | 说明 |
|------|---------|------|
| Blockchain | `/v1/indexer/blockchain/` | 区块链基础 |
| Inscription | `/v1/indexer/inscription/` | 铭文查询 |
| BRC-20 | `/v1/indexer/brc20/` | BRC-20 indexer |
| Runes | `/v1/indexer/runes/` | Runes indexer |
| **Alkanes** | `/v1/indexer/alkanes/` | **Bitcoin 专有** |
| Collection | `/v1/indexer/collection/` | NFT 集合 |
| Inscribe | `/v2/inscribe/` | 铭刻服务 |
| BRC20 Market | `/v3/market/brc20/` | BRC-20 交易 |
| Runes Market | `/v3/market/runes/` | Runes 交易 |
| **Alkanes Market** | `/v3/market/alkanes/` | **Bitcoin 专有** |
| Collection Market | `/v3/market/collection/` | NFT 交易 |
| Domain Market | `/v3/market/domain/` | 域名交易 |

### Fractal 网络 (`https://open-api-fractal.unisat.io`)

| 类别 | 路径前缀 | 说明 |
|------|---------|------|
| Blockchain | `/v1/indexer/blockchain/` | 同 Bitcoin |
| Inscription | `/v1/indexer/inscription/` | 同 Bitcoin |
| BRC-20 | `/v1/indexer/brc20/` | 同 Bitcoin |
| **Runes** | `/v1/indexer/runes/` | **Fractal 也支持!** |
| Collection | `/v1/indexer/collection/` | 同 Bitcoin |
| **链统计** | `/v1/public/fractal/` | **Fractal 专有** |
| Inscribe | `/v2/inscribe/` | 同 Bitcoin |
| BRC20 Market | `/v3/market/brc20/` | 同 Bitcoin |
| **Runes Market** | `/v3/market/runes/` | **Fractal 也有!** |
| Collection Market | `/v3/market/collection/` | 同 Bitcoin |
| Domain Market | `/v3/market/domain/` | 同 Bitcoin |
| **BRC20-Swap** | `/v1/brc20-swap/` | **Fractal 专有** |
| **CAT20-DEX** | `/v1/cat20-dex/` | **Fractal 专有** |
| **CAT Market** | `api.catmarket.io` | **Fractal 专有** |

---

## Bitcoin vs Fractal 功能对比

| 功能 | Bitcoin 主网 | Fractal |
|------|-------------|---------|
| BRC-20 | ✅ | ✅ |
| Runes | ✅ | ✅ |
| Ordinals | ✅ | ✅ |
| **Alkanes** | ✅ | ❌ |
| Collection | ✅ | ✅ |
| Inscribe Service | ✅ | ✅ |
| Marketplace | ✅ | ✅ |
| **BRC20-Swap** | ❌ | ✅ |
| **CAT20** | ❌ | ✅ |
| **CAT20-DEX** | ❌ | ✅ |
| **OP_CAT** | ❌ | ✅ |
| 出块时间 | ~10 分钟 | ~30 秒 |

---

## 网络选择指南

| 场景 | 推荐网络 | 原因 |
|------|---------|------|
| BRC-20（需要流动性） | Bitcoin | 主网生态成熟 |
| Runes 操作 | 两者皆可 | 都支持 |
| Alkanes 操作 | Bitcoin | Fractal 不支持 |
| 低费用 BRC-20 转账 | Fractal | BRC20-Swap 无矿工费 |
| 游戏/高频小额转账 | Fractal | 30 秒出块 + 低费用 |
| CAT20 开发 | Fractal | OP_CAT 仅 Fractal 支持 |
| NFT Collection | 两者皆可 | 都有完整支持 |
