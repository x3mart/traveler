import styles from './TypeTourPage.module.css';
import { TypeTourPageProps } from './TypeTourPage.props';
import cn from 'classnames';
import { P } from '../../components';
import LogoIcon from '/public/TM.svg';
import Link from 'next/link';
import LogoNameIcon from '/public/Logoname.svg';
import LikeIconBlack from '/public/black-like.svg';
import ArrowIcon from '/public/polygon.svg';
import FlagIcon from '/public/Flag.svg';
import LockIcon from '/public/lock-orange.svg';
import SmileIcon from '/public/smile-orange.svg';
import UserIcon from '/public/user-orange.svg';
import DefenderIcon from '/public/defender-orange.svg';
import FacebookIcon from '/public/14.svg';
import TwitterIcon from '/public/15.svg';
import VKIcon from '/public/16.svg';
import InstagramIcon from '/public/17.svg';
import YoutubeIcon from '/public/18.svg';

export const TypeTourPage = ({ children, className, ...props }: TypeTourPageProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.main, className)}
            {...props}
        >
            <header>
                <div className={styles.wrapper}>
                    
                    <div className={styles.header_logo_block}>
                        <div className={styles.header_logo_block_main_icon}>
                            <Link href='/'>
                                <LogoIcon />
                            </Link>
                        </div>
                        <div className={styles.header_logo_block_second_icon}>
                            <Link href='/'>
                                <LogoNameIcon />
                            </Link>
                        </div>
                    </div>

                    <div className={styles.buttons_block}>
                        <div className={styles.buttons_block_find_tour}>Подберите мне тур</div>
                        <div className={styles.buttons_block_travel}>Путешествия</div>
                        <div className={styles.buttons_block_support}>Поддержка</div>
                        <div className={styles.buttons_block_country}><FlagIcon className={styles.flag} {...props}/></div>
                        <div className={styles.buttons_block_currency}>{'\u20bd'} (Rub)</div>
                        <div className={styles.buttons_block_liked}></div>
                    </div>

                    <div className={styles.enter_block}>
                        Вход
                    </div>

                </div>
            </header>
            <main>
                <div className={styles.wrapper}>
                    ok
                </div>                
            </main>
            <footer>
                <div className={styles.wrapper_footer}>
                    <div className={styles.col_1} {...props}>
                        <div className={styles.header_logo_block}>
                            <div className={styles.header_logo_block_main_icon}>
                                <Link href='/'>
                                    <LogoIcon />
                                </Link>
                            </div>
                            <div className={styles.header_logo_block_second_icon}>
                                <Link href='/'>
                                    <LogoNameIcon />
                                </Link>
                            </div>
                        </div>    
                        <p className={styles.paragraph_content} {...props}>Traveler.market — это маркетплейс авторских туров от тревел-экспертов и частных независимых гидов. 
                        Авторские туры — это спонтанные и яркие возможности, предлагающие взять максимум от каждой точки маршрута. 
                        Мы за непринужденный подход к групповым путешествиям, который больше похож на встречу со старыми друзьями.</p>
                        <p className={styles.paragraph_content_underline} {...props}>© 2020 . Traveler.market</p>
                        <p className={styles.paragraph_content_underline} {...props}>Политика конфиденциальности</p>
                        <p className={styles.paragraph_content_underline} {...props}>Публичная оферта</p>
                        <p className={styles.paragraph_content_underline} {...props}>Согласие на обработку персональных данных</p>
                    </div>

                    <div className={styles.col_2} {...props}>
                        <p className={styles.name_paragraph} {...props}>Информация</p>
                        <p className={styles.paragraph_content_underline} {...props}>Как устроен сервис Traveler.market</p>
                        <p className={styles.paragraph_content_underline} {...props}>Подход сообщества Traveler.market</p>
                        <p className={styles.paragraph_content_underline} {...props}>Журнал о путешествиях</p>
                        <p className={styles.paragraph_content_underline} {...props}>Об авторских турах</p>
                        <p className={styles.paragraph_content_underline} {...props}>Отзывы путешественников</p>
                        <p className={styles.paragraph_content_underline} {...props}>Центр помощи</p>
                        <p className={styles.paragraph_content_underline} {...props}>Связаться с нами</p>
                        <p className={styles.paragraph_content_underline} {...props}>Организуйте авторский тур</p>
                        
                    </div>

                    <div className={styles.col_3} {...props}>
                        <p className={styles.name_paragraph} {...props}>Мы заботимся о вас</p>
                        <div className={styles.p_footer_block} {...props}>
                            <div className={styles.p_footer_block_first} {...props}>
                                <LockIcon />
                            </div>
                            <div className={styles.p_footer_block_second} {...props}>
                                <p>Безопасная оплата</p>
                                <p>Бронируйте туры через нашу надежную платежную систему</p>
                            </div>
                        </div>

                        <div className={styles.p_footer_block} {...props}>
                            <div className={styles.p_footer_block_first} {...props}>
                                <SmileIcon />
                            </div>
                            <div className={styles.p_footer_block_second} {...props}>
                                <p>Продуманная спонтанность</p>
                                <p>Маршруты могут адаптироваться под пожелания группы</p>
                            </div>
                        </div>

                        <div className={styles.p_footer_block} {...props}>
                            <div className={styles.p_footer_block_first} {...props}>
                                <UserIcon />
                            </div>
                            <div className={styles.p_footer_block_second} {...props}>
                                <p>Проверенные тревел-эксперты</p>
                                <p>В нашей базе 3 452 гида, которые прошли тщательный отбор</p>
                            </div>
                        </div>

                        <div className={styles.p_footer_block} {...props}>
                            <div className={styles.p_footer_block_first} {...props}>
                                <DefenderIcon />
                            </div>
                            <div className={styles.p_footer_block_second} {...props}>
                                <p>Проверенные тревел-эксперты</p>
                                <p>В нашей базе 3 452 гида, которые прошли тщательный отбор</p>
                            </div>
                        </div>

                        
                    </div>

                    <div className={styles.col_4} {...props}>
                        <p className={styles.name_paragraph} {...props}>Мы в социальных сетях</p>
                        <div className={styles.social_wide} {...props}> 
                            <FacebookIcon />
                            <TwitterIcon />
                            <VKIcon />
                            <InstagramIcon />
                            <YoutubeIcon />
                            <VKIcon />
                            <InstagramIcon />
                            <YoutubeIcon />
                            <FacebookIcon />
                            <TwitterIcon />
                            <VKIcon />
                            <InstagramIcon />
                            <YoutubeIcon />
                            <VKIcon />
                            <InstagramIcon />
                            <YoutubeIcon />
                        </div>
                    </div>
                </div>                
            </footer>
        </div>
    );
};