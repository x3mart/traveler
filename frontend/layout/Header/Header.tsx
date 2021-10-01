import { Button, Logo, LogoName } from '../../components/';
import styles from './Header.module.css';
import { HeaderProps } from './Header.props';
import LikeIconBlack from '/public/black-like.svg';
import FlagIcon from '/public/Flag.svg';
import ArrowIcon from '/public/polygon.svg';
import MenuIcon from '/public/menu.svg';
import cn from 'classnames';

export const Header = ({ className, ...props }: HeaderProps): JSX.Element => {    
    return (
        <div className={styles.wrapper} {...props}>
            <div className={styles.mobile_menu} {...props}>
                <MenuIcon />
            </div>
            <Logo children={undefined} />
            <LogoName color="logo_header" children={undefined} />
            <div className={styles.desktop_header_buttons} {...props}>
                <Button appearance='header_button' traveler_suitcase = 'true'>Подберите мне тур</Button>
                <Button appearance='header_button_travel' arrow='right'>Путешествия</Button>
                <Button appearance='header_button_support' arrow='right'>Поддержка</Button>
                <Button appearance='header_button_country'><FlagIcon className={styles.flag} {...props}/><ArrowIcon /></Button>
                <Button appearance='header_button_currency' arrow='right'>{'\u20bd'} (Rub)</Button>
                <Button appearance='header_button_liked'><LikeIconBlack fill='black' /></Button>
            </div>
            <Button appearance='header_button_enter'>Вход</Button>
        </div>
    );
};