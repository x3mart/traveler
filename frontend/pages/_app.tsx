import { AppProps } from 'next/dist/shared/lib/router/router';
import '../styles/globals.css';
import Head from 'next/head';
import React from 'react';

function MyApp({ Component, pageProps }: AppProps): JSX.Element {
  return <>
      <Head>
        <title></title>
        <meta name="description" content="traveler market" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Component {...pageProps} />
  </>;
}

export default MyApp;
