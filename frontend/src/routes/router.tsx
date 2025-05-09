import { createBrowserRouter } from 'react-router-dom';
import App from '../App';
import Generative from '../generative/generative';
import NotFound from './NotFound';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <NotFound />,
  },
  {
    path: '/generated-ui/:designerId/:personaId',
    element: <Generative />,
  },
]);

export default router;