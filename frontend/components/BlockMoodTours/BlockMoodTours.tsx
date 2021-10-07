import styles from './BlockMoodTours.module.css';
import { BlockMoodToursProps } from './BlockMoodTours.props';
import cn from 'classnames';
import { InfoBlock, Htag } from '..';

export const BlockMoodTours = ({ block_style, children, className, ...props }: BlockMoodToursProps): JSX.Element => {    
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
                            Поиск туров по настроению 
                        </Htag>
                        <Htag tag='h4'>
                            А какое настроение сегодня у вас?
                        </Htag>
                    </InfoBlock>
                    <div className={styles.mood_block} {...props}> 
                        <div className={styles.mood_block_item} {...props}>        
                            <Htag tag='h3'>Автобусные туры</Htag>
                            <Htag tag='h3'>Автотуры</Htag>
                            <Htag tag='h3'>Велотуры</Htag>
                            <Htag tag='h3'>Винные туры</Htag>
                            <Htag tag='h3'>Гастрономические туры</Htag>
                            <Htag tag='h3'>Горнолыжные туры</Htag>
                            <Htag tag='h3'>Городские туры</Htag>
                            <Htag tag='h3'>Дайвинг-туры</Htag>
                            <Htag tag='h3'>Девичник-туры</Htag>
                            <Htag tag='h3'>Детские лагеря</Htag>
                            <Htag tag='h3'>Джип-туры</Htag>                        
                        {/* </div>
                        <div className={styles.mood_block_item} {...props}>           */}
                            <Htag tag='h3'>Железнодорожные туры</Htag>
                            <Htag tag='h3'>Йога-туры</Htag>
                            <Htag tag='h3'>Конные туры</Htag>
                            <Htag tag='h3'>Круизы</Htag>
                            <Htag tag='h3'>Мототуры</Htag>
                            <Htag tag='h3'>Научные туры</Htag>
                            <Htag tag='h3'>Новогодние туры</Htag>
                            <Htag tag='h3'>Обзорные туры</Htag>
                            <Htag tag='h3'>Обучающие туры</Htag>
                            <Htag tag='h3'>Оздоровительные туры</Htag>
                            <Htag tag='h3'>Паломнические туры</Htag>
                        {/* </div>
                        <div className={styles.mood_block_item} {...props}>  */}
                            <Htag tag='h3'>Сафари-туры</Htag>
                            <Htag tag='h3'>Сёрфинг-туры</Htag>
                            <Htag tag='h3'>Спортивные туры</Htag>
                            <Htag tag='h3'>Треккинговые туры</Htag>
                            <Htag tag='h3'>Туристические походы</Htag>
                            <Htag tag='h3'>Туры в горы</Htag>
                            <Htag tag='h3'>Туры на природу</Htag>
                            <Htag tag='h3'>Туры на майские праздники</Htag>
                            <Htag tag='h3'>Туры на море</Htag>
                            <Htag tag='h3'>Туры на полюс</Htag>
                            <Htag tag='h3'>Туры на яхте</Htag>
                        {/* </div>
                        <div className={styles.mood_block_item} {...props}>  */}
                            <Htag tag='h3'>Туры с восхождением в горы</Htag>
                            <Htag tag='h3'>Туры с детьми</Htag>
                            <Htag tag='h3'>Фитнес-туры</Htag>
                            <Htag tag='h3'>Фототуры</Htag>
                            <Htag tag='h3'>Экскурсионные туры</Htag>
                            <Htag tag='h3'>Экспедиционные туры</Htag>
                            <Htag tag='h3'>Экстремальные туры</Htag>
                            <Htag tag='h3'>Этнические туры</Htag>
                        </div>
                    </div>
            </div> 
            
        </div>
    );
};