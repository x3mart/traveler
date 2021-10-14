import styles from './BlockExpertsFeedback.module.css';
import { BlockExpertsFeedbackProps } from './BlockExpertsFeedback.props';
import cn from 'classnames';
import { InfoBlock, Htag, P, Rating } from '..';

export const BlockExpertsFeedback = ({ block_style, children, className, ...props }: BlockExpertsFeedbackProps): JSX.Element => {    
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
                            Отзывы (120) 
                        </Htag>
                        <Htag tag='h4'>
                            Отзывы путешественников
                        </Htag>
                    </InfoBlock>
                    <div className={styles.feedback_experts_block} {...props}>
                        <Rating position='right' children={undefined} />
                        <div className={styles.feedback_experts_block_person} {...props}>
                            <div className={styles.feedback_experts_block_person_ava} {...props}></div>
                            <div className={styles.feedback_experts_block_person_name} {...props}>
                                Мария Киселева <br />
                                <span>Март, 2021</span>
                            </div>
                        </div>
                        <div className={styles.feedback_experts_block_text} {...props}>
                            <div className={styles.feedback_experts_block_text_main} {...props}>
                                Весь Стамбул. Принцевы острова и приключения в Каппадокии. 
                            </div>
                            <div className={styles.feedback_experts_block_text_contetnt} {...props}>
                                Маршрут "Аиды Дивы" построен по уму: день в море сразу после старта, и день в море перед финишем. 
                                Так как возможных точек старта и финиша было две (Ла-Романа и Монтего-Бэй), то и дней в море, соответственно, было четыре ...
                            </div>
                        </div>
                    </div>
                    <div className={styles.feedback_experts_block} {...props}>
                        <Rating position='right' children={undefined} />
                        <div className={styles.feedback_experts_block_person} {...props}>
                            <div className={styles.feedback_experts_block_person_ava} {...props}></div>
                            <div className={styles.feedback_experts_block_person_name} {...props}>
                                Ксения Скоробогатько <br />
                                <span>Апрель, 2021</span>
                            </div>
                        </div>
                        <div className={styles.feedback_experts_block_text} {...props}>
                            <div className={styles.feedback_experts_block_text_main} {...props}>
                                Байкал: приключения на самом большом озере мира 
                            </div>
                            <div className={styles.feedback_experts_block_text_contetnt} {...props}>
                                О туре: "Хотелось бы поблагодарить всю команду за незабываемое путешествие в Стамбул и Каппадокию) Богатая история, 
                                вкусная еда, удивительные ландшафты, рассвет на кабриолетах, уникальная природа, конная прогулка, подземные города, 
                                скалы и долины - оставили яркие впечатления надолго ) Восхититься пейзажами и встретить рассвет в корзине воздушного шара- 
                                определенно одного из самого запоминающегося. Это, определенно, нужно увидеть) Все было на высшем уровне) Особенно хотелось 
                                бы отметить нашу сопровождающую Викторию, которая действительно любит то, что делает , и делает это - отлично! Этот тур - 
                                коллекция всего самого-самого! Все продумано до мелочей ) После такого красивого приключения ещё долго ощущаешь нереальность 
                                происходящего)
                            </div>
                        </div>
                    </div>
                    <div className={styles.feedback_experts_block} {...props}>
                        <Rating position='right' children={undefined} />
                        <div className={styles.feedback_experts_block_person} {...props}>
                            <div className={styles.feedback_experts_block_person_ava} {...props}></div>
                            <div className={styles.feedback_experts_block_person_name} {...props}>
                                Артур  <br />
                                <span>Апрель, 2021</span>
                            </div>
                        </div>
                        <div className={styles.feedback_experts_block_text} {...props}>
                            <div className={styles.feedback_experts_block_text_main} {...props}>
                                Байкал: приключения на самом большом озере мира
                            </div>
                            <div className={styles.feedback_experts_block_text_contetnt} {...props}>
                                О туре: "Неделю назад вернулась из поездки в Турцию. Было круто! Это моя третья поездка с ребятами. 
                                Здорово, что благодаря формату небольшой группы (в нашей было 10 человек) совершенно комфортно можно ехать 
                                одной или с кем-то: в любом случае уже к концу первого дня, на фоне пережитых впечатлений и эмоций, вся группа 
                                превращается в компанию друзей-единомышленников :) Стамбул оказался не похожим ни на один город, где я бывала раньше. 
                                Город из книги ""Тысяча и одна ночь"", но в то же время очень современный. Он впечатляет своим масштабом и очаровывает 
                                многим: своими паромами и морскими прогулками, красотой мечетей, колоритыми улочками с уютными кафешками и сувенирными 
                                магазинчиками, набитыми цветными лампами и восточными коврами, своими набережными с вереницами рыбаков, вездесущими 
                                чайками. И, конечно же, котами - всевозможных размеров и окрасок, они там повсюду! Рекомендую, если есть возможность, 
                                задержаться в городе на несколько дополнительных дней. Однозначно найдётся, чем их занять. Отдельный день можно 
                                планировать на шопинг (главное, помнить про размеры и свободное место в своем чемодане :) ) Каппадокия - это вообще 
                                отдельный мир. Я много раз до поездки видела фото, но все равно не ожидала такой концентрации красоты. 
                                Полет на шаре - одно из самых ярких впечатлений в моей жизни. И прогулка по скалам на лошадях добавила поездке адреналина) 
                                Спасибо, что создаёте в своих поездках атмосферу настоящего путешествия, когда ты не просто турист, расставляющий галочки 
                                напротив списка посещенных достопримечательностей, но и самый настоящий исследователь новой страны или города!
                            </div>
                        </div>
                    </div>
                    <div className={styles.feedback_experts_block_more} {...props}>
                        Показать больше отзывыв о Давиде
                    </div>
                        
                   
            </div> 
            
        </div>
    );
};