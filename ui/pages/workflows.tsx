import Head from 'next/head';
import { Workflows } from '@/components/Workflows/Workflows';

const WorkflowsPage = () => {
  return (
    <>
      <Head>
        <title>Workflows | QCA</title>
      </Head>
      <Workflows />
    </>
  );
};

export default WorkflowsPage;
