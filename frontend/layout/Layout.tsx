import styles from './Layout.module.css';
import { LayoutProps } from './Layout.props';
import cn from 'classnames';
import React, { FunctionComponent } from 'react';
import { Header } from './Header/Header';
import { Footer } from './Footer/Footer';

const Layout = ({ children }: LayoutProps): JSX.Element => {    
    return (
        <div>     
                  
            <Header className={styles.header} />   
                <div className={styles.body}>
                    {children}
                </div>                
            <Footer className={styles.footer} />
                     
        </div>
    );
};

export const withLayout = <T extends Record<string, unknown>>(Component: FunctionComponent<T>) => {
    return function withLayoutComponent(props: T): JSX.Element {
        return (
            <Layout>
                <Component {...props} />
            </Layout>
        )
    }
}