import styles from './CardOnTop.module.css';
import { CardOnTopProps } from './CardOnTop.props';
import cn from 'classnames';
import { Tag, Htag } from '..';
import DoneIcon from '/public/done.svg';
import LikeIcon from '/public/heartblack.svg';
import ClockIcon from '/public/clock.svg';
import PeopleIcon from '/public/people.svg';  
import CalendarIcon from '/public/calendarsmall.svg';
import ArrowGreyIcon from '/public/arrowdowngrey.svg';
import MinusIcon from '/public/minus.svg';
import PlusIcon from '/public/plus.svg';
import StarIcon from '/public/Star.svg';
    


export const CardOnTop = ({ block_style, block_width, children, className, ...props }: CardOnTopProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.card_tour, className, {
                [styles.card_tour]: block_style == 'card_tour',
                [styles.card_tour_border]: block_style == 'card_tour_border',
                [styles.block_width_travel_page]: block_width == 'block_width_travel_page',
                [styles.display_none]: block_width == 'display_none',
            })}
            {...props}
            
        >    
                  
            {children}
            
            <div className={styles.top_card}>
                <div className={styles.top_card_header}>
                    <p className={styles.top_card_header_first}>Зарегистрируйтесь!</p>
                    <p className={styles.top_card_header_second}>И начните путешествовать по новому!</p>
                </div>
                <div className={styles.top_card_guarantee}>
                    <DoneIcon /> <p>Тур проверен и гарантирован</p> <LikeIcon />
                </div>
                <div className={styles.top_card_cost}>
                    <div className={styles.top_card_cost_left}>
                        75.000 {'\u20bd'}
                    </div>
                    <div className={styles.top_card_cost_right}>
                        в день 7.500 {'\u20bd'}
                    </div>
                </div>
                <div className={styles.top_card_info}>
                    Стоимость указана на человека при размещении в двухместном номере в отеле 3*. <span>подробнее</span> 
                </div>
                <div className={styles.top_card_time}>
                    <div className={styles.top_card_time_days}>
                        <div className={styles.top_card_time_days_icon}><ClockIcon /></div>
                        <div className={styles.top_card_time_days_info}>
                            <div className={styles.top_card_time_days_info_head}>
                                Длительность:
                            </div>
                            <div className={styles.top_card_time_days_info_foot}>
                                5 дней
                            </div>
                        </div>
                    </div>
                    <div className={styles.top_card_time_passenger}>
                        <div className={styles.top_card_time_passenger_icon}><PeopleIcon /></div>
                        <div className={styles.top_card_time_passenger_info}>
                            <div className={styles.top_card_time_days_info_head}>
                                Свободно мест:
                            </div>
                            <div className={styles.top_card_time_days_info_foot}>
                                8 из 10
                            </div>
                        </div>
                    </div>
                </div>

                <div className={styles.top_card_buttons}>
                    <div className={styles.top_card_buttons_date}>
                        <CalendarIcon />
                        <div className={styles.top_card_buttons_change_date}>Выберите дату</div>
                        <ArrowGreyIcon className={styles.arrow} />
                    </div>
                    <div className={styles.top_card_buttons_seats}>
                        <div className={styles.top_card_buttons_minus}><MinusIcon /></div>
                        <div className={styles.top_card_buttons_change_seats}>1 место</div>
                        <div className={styles.top_card_buttons_plus}><MinusIcon /><PlusIcon className={styles.plus} /></div>
                    </div>
                    <div className={styles.top_card_buttons_accept}>
                        Хочу поехать
                    </div>
                </div>

                <div className={styles.top_card_booking_info}>
                    <div className={styles.top_card_booking_info_head}>Для бронирования тура достаточно 8 750 {'\u20bd'}</div>
                    <div className={styles.top_card_booking_info_foot}>При отмене бронирования любого путешествия в течение 24 часов после оплаты вы получаете полный возврат.</div>
                </div>

                <div className={styles.top_card_author}>
                    <div className={styles.card_tour_content_guide_info_name_raiting}>
                        <div className={styles.card_tour_content_guide_info_name_avatar}>

                        </div>
                        <div className={styles.card_tour_content_guide_info_name_avatar_info}>
                            <Htag tag='h4'>Мария <span className={styles.author_span}>Автор тура</span></Htag>
                            <Htag tag='h4'>
                                <StarIcon />
                                <span className={styles.raiting_star}>4.9</span>
                                (132)  
                            </Htag>
                        </div>
                        
                    </div>
                    <div className={styles.top_card_author_button}>
                        Написать автору тура
                    </div>
                </div>
            </div>
             
        </div>
    );
};