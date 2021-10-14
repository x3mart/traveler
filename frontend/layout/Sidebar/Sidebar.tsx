import styles from './Sidebar.module.css';
import { SidebarProps } from './Sidebar.props';
import cn from 'classnames';
import { Tag, Htag } from '../../components';
import DoneIcon from '/public/done.svg';
import LikeIcon from '/public/heartblack.svg';
import ClockIcon from '/public/clock.svg';
import PeopleIcon from '/public/people.svg';  
import CalendarIcon from '/public/calendarsmall.svg';
import ArrowGreyIcon from '/public/arrowdowngrey.svg';
import MinusIcon from '/public/minus.svg';
import PlusIcon from '/public/plus.svg';
import StarIcon from '/public/Star.svg';
    


export const Sidebar = ({ block_style, block_width, children, className, ...props }: SidebarProps): JSX.Element => {    
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
            
            <div className={styles.top_card} {...props}>
                <div className={styles.top_card_header} {...props}>
                    <p className={styles.top_card_header_first} {...props}>Зарегистрируйтесь!</p>
                    <p className={styles.top_card_header_second} {...props}>И начните путешествовать по новому!</p>
                </div>
                <div className={styles.top_card_guarantee} {...props}>
                    <DoneIcon /> <p>Тур проверен и гарантирован</p> <LikeIcon />
                </div>
                <div className={styles.top_card_cost} {...props}>
                    <div className={styles.top_card_cost_left} {...props}>
                        75.000 {'\u20bd'}
                    </div>
                    <div className={styles.top_card_cost_right} {...props}>
                        в день 7.500 {'\u20bd'}
                    </div>
                </div>
                <div className={styles.top_card_info} {...props}>
                    Стоимость указана на человека при размещении в двухместном номере в отеле 3*. <span>подробнее</span> 
                </div>
                <div className={styles.top_card_time} {...props}>
                    <div className={styles.top_card_time_days} {...props}>
                        <div className={styles.top_card_time_days_icon} {...props}><ClockIcon /></div>
                        <div className={styles.top_card_time_days_info} {...props}>
                            <div className={styles.top_card_time_days_info_head} {...props}>
                                Длительность:
                            </div>
                            <div className={styles.top_card_time_days_info_foot} {...props}>
                                5 дней
                            </div>
                        </div>
                    </div>
                    <div className={styles.top_card_time_passenger} {...props}>
                        <div className={styles.top_card_time_passenger_icon} {...props}><PeopleIcon /></div>
                        <div className={styles.top_card_time_passenger_info} {...props}>
                            <div className={styles.top_card_time_days_info_head} {...props}>
                                Свободно мест:
                            </div>
                            <div className={styles.top_card_time_days_info_foot} {...props}>
                                8 из 10
                            </div>
                        </div>
                    </div>
                </div>

                <div className={styles.top_card_buttons} {...props}>
                    <div className={styles.top_card_buttons_date} {...props}>
                        <CalendarIcon />
                        <div className={styles.top_card_buttons_change_date} {...props}>Выберите дату</div>
                        <ArrowGreyIcon className={styles.arrow} {...props} />
                    </div>
                    <div className={styles.top_card_buttons_seats} {...props}>
                        <div className={styles.top_card_buttons_minus} {...props}><MinusIcon /></div>
                        <div className={styles.top_card_buttons_change_seats} {...props}>1 место</div>
                        <div className={styles.top_card_buttons_plus} {...props}><MinusIcon /><PlusIcon className={styles.plus} {...props} /></div>
                    </div>
                    <div className={styles.top_card_buttons_accept} {...props}>
                        Хочу поехать
                    </div>
                </div>

                <div className={styles.top_card_booking_info} {...props}>
                    <div className={styles.top_card_booking_info_head} {...props}>Для бронирования тура достаточно 8 750 {'\u20bd'}</div>
                    <div className={styles.top_card_booking_info_foot} {...props}>При отмене бронирования любого путешествия в течение 24 часов после оплаты вы получаете полный возврат.</div>
                </div>

                <div className={styles.top_card_author} {...props}>
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
                    <div className={styles.top_card_author_button} {...props}>
                        Написать автору тура
                    </div>
                </div>
            </div>
             
        </div>
    );
};