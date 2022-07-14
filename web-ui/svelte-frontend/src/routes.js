import Home from './routes/Home.svelte';
// import Lorem from './routes/Lorem.svelte';
import MongoDB from './routes/MongoDB.svelte';
import Messages from './routes/Messages.svelte';
import NotFound from './routes/NotFound.svelte';

export default {
    '/': Home,
    '/mongo': MongoDB,
    '/messages': Messages,
    // '/lorem/:repeat': Lorem,
    // The catch-all route must always be last
    '*': NotFound
};
