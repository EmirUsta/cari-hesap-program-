import { useState, useEffect } from 'react';
import api from '../api';

export default function POSView() {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState('');
  const [cart, setCart] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [selectedCustomerId, setSelectedCustomerId] = useState('');
  const [transactionType, setTransactionType] = useState('sale');
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    // Fetch initial data
    const fetchData = async () => {
      try {
        const prodRes = await api.get('/products/');
        setProducts(prodRes.data);

        const custRes = await api.get('/customers/');
        setCustomers(custRes.data);
        if (custRes.data.length > 0) {
          setSelectedCustomerId(custRes.data[0].id);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);

  const filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.barcode.includes(search)
  );

  const addToCart = (product) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item => item.id === product.id ? { ...item, qty: item.qty + 1 } : item);
      }
      return [...prev, { ...product, qty: 1 }];
    });
  };

  const removeFromCart = (productId) => {
    setCart(prev => prev.filter(item => item.id !== productId));
  };

  const totalAmount = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);

  const handleCheckout = async () => {
    if (cart.length === 0) return alert('Cart is empty!');
    if (!selectedCustomerId) return alert('Please select a customer.');

    try {
      await api.post('/transactions/', {
        customer_id: parseInt(selectedCustomerId),
        transaction_type: transactionType,
        amount: totalAmount,
        description: `POS Checkout - ${cart.length} items`
      });
      setCart([]);
      setSuccessMsg('Transaction completed successfully!');
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (error) {
      console.error("Checkout failed:", error);
      alert('Checkout failed.');
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Product Selection Area */}
      <div className="w-2/3 p-6 flex flex-col">
        <h2 className="text-3xl font-bold mb-4">Products</h2>
        <input
          type="text"
          placeholder="Search by name or barcode..."
          className="p-3 border rounded-lg mb-6 shadow-sm w-full"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <div className="grid grid-cols-3 gap-4 overflow-y-auto">
          {filteredProducts.map(p => (
            <div
              key={p.id}
              onClick={() => addToCart(p)}
              className="bg-white p-4 rounded-lg shadow cursor-pointer hover:bg-blue-50 hover:border-blue-500 border border-transparent transition"
            >
              <h3 className="font-bold text-lg">{p.name}</h3>
              <p className="text-gray-500 text-sm">Barcode: {p.barcode}</p>
              <p className="text-green-600 font-bold mt-2">${p.price.toFixed(2)}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Cart & Checkout Area */}
      <div className="w-1/3 bg-white p-6 shadow-xl flex flex-col">
        <h2 className="text-3xl font-bold mb-4">Current Cart</h2>

        <div className="flex-1 overflow-y-auto mb-4 border-b border-gray-200">
          {cart.length === 0 ? (
            <p className="text-gray-500 italic text-center mt-10">Cart is empty</p>
          ) : (
            <ul className="space-y-4">
              {cart.map(item => (
                <li key={item.id} className="flex justify-between items-center p-2 hover:bg-gray-50 rounded">
                  <div>
                    <span className="font-bold">{item.name}</span>
                    <span className="text-sm text-gray-500 ml-2">x{item.qty}</span>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="font-bold">${(item.price * item.qty).toFixed(2)}</span>
                    <button onClick={() => removeFromCart(item.id)} className="text-red-500 font-bold hover:text-red-700">X</button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="mt-auto space-y-4">
          <div className="flex justify-between text-xl font-bold">
            <span>Total:</span>
            <span>${totalAmount.toFixed(2)}</span>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Customer</label>
            <select
              className="w-full border rounded-lg p-2"
              value={selectedCustomerId}
              onChange={(e) => setSelectedCustomerId(e.target.value)}
            >
              <option value="">-- Select Customer --</option>
              {customers.map(c => (
                <option key={c.id} value={c.id}>{c.full_name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Transaction Type</label>
            <select
              className="w-full border rounded-lg p-2"
              value={transactionType}
              onChange={(e) => setTransactionType(e.target.value)}
            >
              <option value="sale">Sale</option>
              <option value="debt">Debt</option>
            </select>
          </div>

          <button
            onClick={handleCheckout}
            disabled={cart.length === 0 || !selectedCustomerId}
            className={`w-full py-4 text-white font-bold text-xl rounded-lg shadow transition ${
              cart.length === 0 || !selectedCustomerId ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700'
            }`}
          >
            Checkout
          </button>

          {successMsg && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative text-center">
              {successMsg}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}