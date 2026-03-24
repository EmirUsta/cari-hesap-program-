import { useState } from 'react';
import api from '../api';

export default function CustomerForm({ onCustomerAdded }) {
  const [formData, setFormData] = useState({ full_name: '', email: '', phone: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/customers/', formData);
      setFormData({ full_name: '', email: '', phone: '' });
      if (onCustomerAdded) onCustomerAdded();
    } catch (error) {
      console.error("Failed to add customer:", error);
    }
  };

  return (
    <div className="p-4 bg-gray-50 rounded-lg shadow mt-4">
      <h3 className="text-xl font-bold mb-4">Add New Customer</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Full Name</label>
          <input
            type="text" required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.full_name}
            onChange={(e) => setFormData({...formData, full_name: e.target.value})}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Phone</label>
          <input
            type="text"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
          />
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Add Customer</button>
      </form>
    </div>
  );
}