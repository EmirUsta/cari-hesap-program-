import { useState } from 'react';
import CustomerList from './components/CustomerList';
import CustomerForm from './components/CustomerForm';
import ProductList from './components/ProductList';
import ProductForm from './components/ProductForm';

function App() {
  const [refreshCustomer, setRefreshCustomer] = useState(0);
  const [refreshProduct, setRefreshProduct] = useState(0);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <h1 className="text-4xl font-extrabold text-gray-900 text-center mb-8">Admin Panel</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <CustomerList key={`c-${refreshCustomer}`} />
            <CustomerForm onCustomerAdded={() => setRefreshCustomer(c => c + 1)} />
          </div>
          <div>
            <ProductList key={`p-${refreshProduct}`} />
            <ProductForm onProductAdded={() => setRefreshProduct(p => p + 1)} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;