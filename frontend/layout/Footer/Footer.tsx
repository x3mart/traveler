import styles from './Footer.module.css';
import { FooterProps } from './Footer.props';
import cn from 'classnames';
import { Logo, LogoName } from '../../components';

export const Footer = ({ className, ...props }: FooterProps): JSX.Element => {    
    return (
        <div className={styles.footer} {...props}> 
            <div className={styles.wrapper} {...props}>
                <Logo />
                <LogoName color="logo_footer" />
            </div>
        </div>
    );
};