import styles from './Footer.module.css';
import { FooterProps } from './Footer.props';
import cn from 'classnames';
import { Logo, LogoName, P, Social } from '../../components';
import LockIcon from '/public/lock-orange.svg';
import SmileIcon from '/public/smile-orange.svg';
import UserIcon from '/public/user-orange.svg';
import DefenderIcon from '/public/defender-orange.svg';

export const Footer = ({ className, ...props }: FooterProps): JSX.Element => {    
    return (
        <div className={styles.footer} {...props}> 
            <div className={styles.wrapper} {...props}>
                <div className={styles.col_1} {...props}>
                    <div className={styles.footer_logo_block} {...props}>
                        <Logo />
                        <LogoName color="logo_footer" />
                    </div>
                    <P color='p_footer'>Traveler.market — это маркетплейс авторских туров от тревел-экспертов и частных независимых гидов. 
                    Авторские туры — это спонтанные и яркие возможности, предлагающие взять максимум от каждой точки маршрута. 
                    Мы за непринужденный подход к групповым путешествиям, который больше похож на встречу со старыми друзьями.</P>
                    <P color='p_footer' link='p_footer_link'>© 2020 . Traveler.market</P>
                    <P color='p_footer' href='' link='p_footer_link'>Политика конфиденциальности</P>
                    <P color='p_footer' href='' link='p_footer_link'>Публичная оферта</P>
                    <P color='p_footer' href='' link='p_footer_link'>Согласие на обработку персональных данных</P>
                </div>

                <div className={styles.col_2} {...props}>
                    <P color='p_footer' link='p_footer_letter_spacing'>Информация</P>
                    <P color='p_footer' link='p_footer_link_col_2'>Как устроен сервис Traveler.market</P>
                    <P color='p_footer' link='p_footer_link_col_2'>Подход сообщества Traveler.market</P>
                    <P color='p_footer' link='p_footer_link_col_2'>Журнал о путешествиях</P>
                    <P color='p_footer' link='p_footer_link_col_2'>Об авторских турах</P>
                    <P color='p_footer' link='p_footer_link_col_2'>Отзывы путешественников</P>
                    <P color='p_footer' link='p_footer_link_col_2'>Центр помощи</P>
                    <P color='p_footer' link='p_footer_link_col_2'>Связаться с нами</P>
                    <P color='p_footer' link='p_footer_link_col_2'>Организуйте авторский тур</P>
                    <P color='p_footer' link='p_footer_letter_spacing_margin_top'>Мы в социальных сетях</P>
                    <Social size='social_wide' />
                </div>

                <div className={styles.col_3} {...props}>
                    <P color='p_footer' link='p_footer_letter_spacing'>Мы заботимся о вас</P>
                    <div className={styles.p_footer_block} {...props}>
                        <div className={styles.p_footer_block_first} {...props}>
                            <LockIcon />
                        </div>
                        <div className={styles.p_footer_block_second} {...props}>
                            <P color='p_footer' link='p_footer_letter_spacing'>Безопасная оплата</P>
                            <P color='p_footer' link='p_footer_link'>Бронируйте туры через нашу надежную платежную систему</P>
                        </div>
                    </div>

                    <div className={styles.p_footer_block} {...props}>
                        <div className={styles.p_footer_block_first} {...props}>
                            <SmileIcon />
                        </div>
                        <div className={styles.p_footer_block_second} {...props}>
                            <P color='p_footer' link='p_footer_letter_spacing'>Продуманная спонтанность</P>
                            <P color='p_footer' link='p_footer_link'>Маршруты могут адаптироваться под пожелания группы</P>
                        </div>
                    </div>

                    <div className={styles.p_footer_block} {...props}>
                        <div className={styles.p_footer_block_first} {...props}>
                            <UserIcon />
                        </div>
                        <div className={styles.p_footer_block_second} {...props}>
                            <P color='p_footer' link='p_footer_letter_spacing'>Проверенные тревел-эксперты</P>
                            <P color='p_footer' link='p_footer_link'>В нашей базе 3 452 гида, которые прошли тщательный отбор</P>
                        </div>
                    </div>

                    <div className={styles.p_footer_block} {...props}>
                        <div className={styles.p_footer_block_first} {...props}>
                            <DefenderIcon />
                        </div>
                        <div className={styles.p_footer_block_second} {...props}>
                            <P color='p_footer' link='p_footer_letter_spacing'>Проверенные тревел-эксперты</P>
                            <P color='p_footer' link='p_footer_link'>В нашей базе 3 452 гида, которые прошли тщательный отбор</P>
                        </div>
                    </div>
                    
                    
                </div>
                
            </div>
        </div>
    );
};