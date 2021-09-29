import styles from './BlockAdvantage.module.css';
import { BlockAdvantageProps } from './BlockAdvantage.props';
import cn from 'classnames';
import { InfoBlock, Htag } from '..';
import LockIconBig from '/public/lock-big.svg';
import SmileIconBig from '/public/smile-big.svg';
import UserIconBig from '/public/user-big.svg';
import DefendIconBig from '/public/Defend.svg';

export const BlockAdvantage = ({ block_style, children, className, ...props }: BlockAdvantageProps): JSX.Element => {     
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <InfoBlock border_color='blue_left_border'>
                        <Htag tag='h2'>
                            Traveler.market - Мы работаем для вас
                        </Htag>
                        <Htag tag='h4'>
                            Основные принципы нашей работы
                        </Htag>
                    </InfoBlock> 
                    <div className={styles.advantage_block}>
                        <div className={styles.advantage_block_item}>
                            <LockIconBig />
                            <Htag tag='h2'>
                                Безопасная оплата
                            </Htag>
                            <Htag tag='h4'>
                                Бронируйте туры через нашу надежную платежную систему
                            </Htag>
                        </div>
                        <div className={styles.advantage_block_item}>
                            <SmileIconBig />
                            <Htag tag='h2'>
                                Продуманная спонтанность
                            </Htag>
                            <Htag tag='h4'>
                                Маршруты могут адаптироваться под пожелания группы
                            </Htag>
                        </div>
                        <div className={styles.advantage_block_item}>
                            <UserIconBig />
                            <Htag tag='h2'>
                                Проверенные тревел-эксперты
                            </Htag>
                            <Htag tag='h4'>
                                В нашей базе 3 452 гида, которые прошли тщательный отбор
                            </Htag>
                        </div>
                        <div className={styles.advantage_block_item}>
                            <DefendIconBig />
                            <Htag tag='h2'>
                                Гарантированные туры
                            </Htag>
                            <Htag tag='h4'>
                                У нас вы найдете более 11 534 туров с гарантированным отправлением
                            </Htag>
                        </div>
                    </div>
                    <div className={styles.advantage_block_item_info}>
                            <Htag tag='h4'>
                                Traveler.market — это маркетплейс авторских туров от тревел-экспертов и частных независимых гидов. 
                                Авторские туры — это спонтанные и яркие <br /> возможности, предлагающие взять максимум от каждой точки маршрута. 
                                Мы за непринужденный подход к групповым путешествиям, который больше <br /> похож на встречу со старыми друзьями.
                            </Htag>
                    </div>
            </div> 
            
        </div>
    );
};