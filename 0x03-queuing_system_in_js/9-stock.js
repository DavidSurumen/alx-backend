import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const listProducts = [
  { itemId: 1, itemName: "Suitcase 250", price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: "Suitcase 450", price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: "Suitcase 650", price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: "Suitcase 1050", price: 550, initialAvailableQuantity: 5 }
];

function getItemById(id) {
  // will return the item from 'listProducts' with the same id
  for (const item of listProducts) {
    if (item.itemId === id) {
      return { ...item };
    }
  }
}

const app = express();
app.listen(1245);

app.get('/list_products', (_req, res) => {
  res.send(JSON.stringify(listProducts));
});

function redisConnector() {
  const client = createClient();

  client.on('error', (err) => {
    console.error('Redis client not connected to the server:', err);
    return;
  });
  return client;
}

function reserveStockById(itemId, stock) {
  // sets in Redis the stock for the key item.ITEM_ID
  const client = redisConnector();

  client.incrby('item.' + itemId, stock);

  if (client.connected) {
    client.quit();
  }
}

async function getCurrentReservedStockById(itemId) {
  const client = redisConnector();
  const getAsync = promisify(client.get).bind(client);

  try {
    const stock = await getAsync('item.' + itemId);

    return stock;
  } catch (err) {
    console.error('Error getting item: ', err);
  }

  if (client.connected)
    client.quit();
}

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);

  if (product) {
    const prod = { ...product };
    const reserved = await getCurrentReservedStockById(itemId);
    if (reserved)
        prod.currentQuantity = product.initialAvailableQuantity > 0 ?
        product.initialAvailableQuantity - reserved : 0;
    else
      prod.currentQuantity = product.initialAvailableQuantity;

    res.send(JSON.stringify(prod));
  } else {
    res.send({"status":"Product not found"});
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);

  if (!product) {
    res.send(JSON.stringify({"status":"Product not found"}));
  } else {
    const available = product.initialAvailableQuantity - await getCurrentReservedStockById(itemId);
    if (available < 1) {
      res.send(JSON.stringify({"status": "Not enough stock available", "itemId": itemId}));
    } else {
      reserveStockById(itemId, 1);
      res.send(JSON.stringify({"status": "Reservation confirmed", "itemId": itemId}));
    }
  }
});
