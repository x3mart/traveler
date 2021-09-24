
import React from 'react';
import { Button, Htag, P, Tag } from '../components';
import { withLayout } from '../layout/Layout';


function Home(): JSX.Element {   
  return ( 
    <>       
        
        <Htag tag='h1'>traveler market - Маркетплейс авторских туров</Htag>
        <Button appearance='primary'>Подобрать тур</Button>
        <Button appearance='ghost'>Читать полностью</Button>
        <P>Traveler.market — это маркетплейс авторских туров от тревел-экспертов и частных независимых гидов. 
          Авторские туры — это спонтанные и яркие возможности, предлагающие взять максимум от каждой точки маршрута. 
          Мы за непринужденный подход к групповым путешествиям, который больше похож на встречу со старыми друзьями.</P>
        <P color='p_footer'>Traveler.market — это маркетплейс авторских туров от тревел-экспертов и частных независимых гидов. 
          Авторские туры — это спонтанные и яркие возможности, предлагающие взять максимум от каждой точки маршрута. 
          Мы за непринужденный подход к групповым путешествиям, который больше похож на встречу со старыми друзьями.</P>
        <Tag size='s'></Tag>
        <Tag size='s'></Tag>
        <Tag size='s'></Tag>
        <Tag size='s'></Tag>
        <Tag size='m'></Tag>
        <Tag size='m'></Tag>
        <Tag size='m'></Tag>        
        <Tag size='b'></Tag>
        <Tag size='b'></Tag>
        <Tag size='l'></Tag>   
    </>
  );
}

export default withLayout(Home);