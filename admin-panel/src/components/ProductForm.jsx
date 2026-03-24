import { useState } from 'react';
import api from '../api';

export default function ProductForm({ onProductAdded }) {
  const [formData, setFormData] = useState({ name: '', barcode: '', price: 0, stock_quantity: 0 });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/products/', formData);
      setFormData({ name: '', barcode: '', price: 0, stock_quantity: 0 });
      if (onProductAdded) onProductAdded();
    } catch (error) {
      console.error("Failed to add product:", error);
    }
  };

  return (
    <div className="p-4 bg-gray-50 rounded-lg shadow mt-4">
      <h3 className="text-xl font-bold mb-4">Add New Product</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Name</label>
          <input
            type="text" required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Barcode</label>
          <input
            type="text" required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.barcode}
            onChange={(e) => setFormData({...formData, barcode: e.target.value})}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Price ($)</label>
          <input
            type="number" step="0.01" required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.price}
            onChange={(e) => setFormData({...formData, price: parseFloat(e.target.value)})}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Stock</label>
          <input
            type="number" required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.stock_quantity}
            onChange={(e) => setFormData({...formData, stock_quantity: parseInt(e.target.value)})}
          />
        </div>
        <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Add Product</button>
      </form>
    </div>
  );
}