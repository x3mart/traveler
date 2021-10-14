import styles from './BlockTourOverview.module.css';
import { BlockTourOverviewProps } from './BlockTourOverview.props';
import cn from 'classnames';
import DoneIcon from '../../public/done.svg';
import CancelIcon from '../../public/cancel.svg';
import { Htag, P } from '..';
import PlayButtonIcon from '../../public/play-button.svg';
import ArrowUp from '../../public/arrowgreenup.svg';
import ArrowDown from '../../public/arrowgreendown.svg';
import StarBigIcon from '/public/star-big.svg';



export const BlockTourOverview = ({ block_style, children, className, ...props }: BlockTourOverviewProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                        <Htag tag='h2'>
                            Обзор тура
                        </Htag>
                        <P>
                            Если у вас всего неделя отпуска,а вам хотелось бы побывать в горах , вдохнуть полной грудью морской воздух или ощутить под ногами пески 
                            бархана, то вам нужен наш тур "Сокровища Дагестана"!
                        </P>
                        <P>
                            За 5 дней вы получите незабываемые ощущения от всего вышеперечисленного,находясь всего лишь на землях красивейшей республики нашей 
                            страны-Дагестана.
                        </P>
                        <P>
                            Вы посетите все локации,которые обязаны к просмотру при путешествии в Дагестан и даже более того, ведь Дагестан богат не только 
                            природными красотами,но и многовековой историей, погружению в  которую мы посвятили отдельный день.
                        </P>
                        <P>
                            Большим преимуществом НАШЕГО тура является ВАША свобода действий,чтобы вы могли получить удовольствие от каждого момента,проведенного 
                            в туре,раскрепоститься и прочувствовать наслаждение каждой клеточкой тела: встретить первые лучики солнца, услышать шелест горных трав 
                            на ветру, затаив дыхание, наблюдать за парящим орлом, а вечером в теплой дружеской компании наслаждаться душевными песнями у костра
                        </P>    

                        <Htag tag='h2'>
                            Чем мы займемся в туре
                        </Htag>  
                        <P>Мы пустимся в весёлые приключения на джипах по Дагестану!</P>
            </div>
            <div className={styles.wrapper_custom} {...props}>
                        <div className={styles.overview_video_block} {...props}>            
                            <PlayButtonIcon />
                        </div>
            </div>
            <div className={styles.wrapper} {...props}>
                        <P>
                            Будем открывать чарующе красивые и труднодоступные уголки с первозданной природой! Наш путь проложен по старинным живописным дорогам, а иногда и бездорожью, 
                            и все для того, чтобы добраться туда, где Вам не будет мешать толпа туристов. 
                        </P>
            </div>
            <div className={styles.wrapper_custom} {...props}>
                        <div className={styles.overview_photo_block_1} {...props}></div>
            </div>
            <div className={styles.wrapper} {...props}>
                        <P>
                            На протяжении всего путешествия вас ждут сотни локаций для исключительных фотографий, которые удивят ваших друзей и близких, 
                            а возможно и вдохновят на увлекательное путешествие по Дагестану
                        </P>
            </div>
            <div className={styles.wrapper_custom} {...props}>
                        <div className={styles.overview_photo_block_2} {...props}></div>
            </div>
            <div className={styles.wrapper} {...props}>
                        <P>
                            Вы увидите Сулакский каньон под другим углом, прикоснётесь к уникальным старинным сооружениям , 
                            почувствуете силу времени, ступив на земли древних заброшенные сел-призраков, ощутите мощь горных рек и водопадов.
                        </P>
            </div>
            <div className={styles.wrapper_custom} {...props}>
                        <div className={styles.overview_photo_block_3} {...props}></div>
            </div>
            <div className={styles.wrapper} {...props}>
                        <P>
                            А еще мы уверены, что "путь к Сердцу Дагестана  лежит через желудок". Национальная кухня заслуживает 
                            чуть ли не главное место в нашем туре! Свежайшее мясо и блюда из них, молоко, сметана, хлеб.
                        </P>
                        <P>Вы удивитесь, насколько другой вкус у действительно натуральных продуктов</P>
            </div>
            <div className={styles.wrapper_custom} {...props}>
                        <div className={styles.overview_photo_block_4} {...props}></div>
            </div>
            <div className={styles.wrapper} {...props}>
                        <P>
                            Данный тур разработан таким образом, что участники практически не ограничены в передвижении по локациям, мы даем свободу,чтобы вы могли насладиться моментом : 
                        </P>
                        <P>Данный тур разработан таким образом,что участники практически не ограничены в передвижении по локациям, мы даем свободу,чтобы вы могли насладиться моментом :</P>  

                        <P>С улыбкой встретить первые лучи солнца;</P> 

                        <P>Затаив дыхание проводить закат;</P>  

                        <P>Чтобы вы могли надышаться горным воздухом</P>  

                        <P>Очароваться звездной россыпью на небе</P>

                        <div className={styles.overview_photo_gallery} {...props}>
                            <Htag tag='h2'>
                                Галерея
                            </Htag>
                        </div>
            </div>
            <div className={styles.wrapper_custom} {...props}>
                            <div className={styles.overview_photo_gallery_items} {...props}>
                                <div className={styles.overview_photo_gallery_item} {...props}></div>
                                <div className={styles.overview_photo_gallery_item} {...props}></div>
                                <div className={styles.overview_photo_gallery_item} {...props}></div>
                                <div className={styles.overview_photo_gallery_item} {...props}></div>
                                <div className={styles.overview_photo_gallery_item} {...props}></div>
                                <div className={styles.overview_photo_gallery_item} {...props}></div>
                                <div className={styles.overview_photo_gallery_item} {...props}></div>
                                <div className={styles.overview_photo_gallery_item} {...props}></div>
                                <div className={styles.overview_photo_gallery_item} {...props}></div>
                            </div>
            </div>
            
            <div className={styles.wrapper} {...props}>
                        <div className={styles.rout_travel_block} {...props}>
                            <Htag tag='h2'>
                                Маршрут
                            </Htag>
                        </div>    
            </div>
            <div className={styles.wrapper_custom} {...props}>
                            <div className={styles.rout_travel_block_item} {...props}></div>  
            </div>                       
            <div className={styles.wrapper} {...props}>           
                            <div className={styles.rout_travel_block_info} {...props}>
                                <div className={styles.rout_travel_block_info_start} {...props}>
                                    <span className={styles.rout_travel_block_info_start_head} {...props}>Старт</span><br />
                                    <span className={styles.rout_travel_block_info_start_foot} {...props}>12 апреля, Махачкала, 08:00 по местному времени</span>
                                </div>
                                <div className={styles.rout_travel_block_info_finish} {...props}>
                                    <span className={styles.rout_travel_block_info_start_head} {...props}>Финиш</span><br />
                                    <span className={styles.rout_travel_block_info_start_foot} {...props}>16 апреля, Махачкала, 20:00 по местному времени</span>
                                </div>                            
                            </div>
            </div>
            <div className={styles.wrapper_custom} {...props}>
                        <div className={styles.rout_travels_day_block} {...props}>                            
                            <div className={styles.rout_travels_day_main_card} {...props}>
                                <div className={styles.rout_travels_day_main_card_image} {...props}></div>
                                <div className={styles.rout_travels_day_main_card_info} {...props}>
                                    <div className={styles.rout_travels_day_main_card_info_header} {...props}>
                                        <Htag tag='h2'>
                                            День 1 . Визитные карточки Дагестана (Сулак, Сарыкум)
                                        </Htag>
                                        <ArrowUp />
                                    </div>
                                    <div className={styles.rout_travels_day_main_card_info_text} {...props}>
                                        <P>
                                            Всей группой дружно встречаемся в Махачкале и выезжаем в сторону Сулакского каньона. 
                                            По пути мы сделаем остановку и посетим природный феномен, песчаный заповедник Бархан Сарыкум. 
                                            После экскурсии по песчаному гиганту держим путь на уникальную смотровую площадку на верхней части части каньона, 
                                            где открывается невероятный вид на лазурные изгибы реки Сулак, а после спускаемся прямиком к водам каньона,чтобы покататься на катерах по бирюзовой глади.
                                            По завершению знакомства с Сулакским каньоном мы отправляемся в Верхний Гуниб к месту дальнейшего проживания, и по пути заглянем на смотровую площадку с панорамой на Чиркейскую ГЭС.
                                        </P>
                                    </div>
                                </div>
                            </div>
                            <div className={styles.rout_travels_day_card} {...props}>
                                <div className={styles.rout_travels_day_main_card_info_header} {...props}>
                                    <Htag tag='h2'>
                                        День 2 . Жемчужины Дагестана
                                    </Htag>
                                    <ArrowDown />
                                </div>
                                <div className={styles.rout_travels_day_main_card_info_text} {...props}></div>
                            </div>
                            <div className={styles.rout_travels_day_card} {...props}>
                                <div className={styles.rout_travels_day_main_card_info_header} {...props}>
                                    <Htag tag='h2'>
                                        День 3 . Гуниб-сердце Дагестана ; аул-призрак Гамсутль
                                    </Htag>
                                    <ArrowDown />
                                </div>
                                <div className={styles.rout_travels_day_main_card_info_text} {...props}></div>
                            </div>
                            <div className={styles.rout_travels_day_card} {...props}>
                                <div className={styles.rout_travels_day_main_card_info_header} {...props}>
                                    <Htag tag='h2'>
                                        День 4 . Салтинский водопад и село гончаров Балхар
                                    </Htag>
                                    <ArrowDown />
                                </div>
                                <div className={styles.rout_travels_day_main_card_info_text} {...props}></div>
                            </div>
                            <div className={styles.rout_travels_day_card} {...props}>
                                <div className={styles.rout_travels_day_main_card_info_header} {...props}>
                                    <Htag tag='h2'>
                                        День 5 . Путь 
                                    </Htag>
                                    <ArrowDown />
                                </div>
                                <div className={styles.rout_travels_day_main_card_info_text} {...props}></div>
                            </div>
                        </div>
            </div>
            <div className={styles.wrapper} {...props}> 
                        <div className={styles.type_hotel_room} {...props}>
                            <Htag tag='h2'>
                                Тип размещения
                            </Htag>
                            <div className={styles.type_hotel_room_text} {...props}>
                                <P>Гостевые домики</P>
                                <P>Гостиницы 3*</P>
                            </div> 
                        </div>
            

                        <div className={styles.gallery_hotel_room} {...props}>
                            <Htag tag='h2'>
                                Фото мест проживания
                            </Htag>
            
                        </div>
            </div>
            <div className={styles.wrapper_custom} {...props}>
                        <div className={styles.gallery_hotel_room_items} {...props}>
                            <div className={styles.gallery_hotel_room_item} {...props}></div>
                            <div className={styles.gallery_hotel_room_item} {...props}></div>
                            <div className={styles.gallery_hotel_room_item} {...props}></div>
                            <div className={styles.gallery_hotel_room_item} {...props}></div>
                            <div className={styles.gallery_hotel_room_item} {...props}></div>
                            <div className={styles.gallery_hotel_room_item} {...props}></div>
                        </div> 
            </div>
            <div className={styles.wrapper} {...props}> 
                        <div className={styles.include_block} {...props}>
                            <Htag tag='h2'>
                                В стоимость включено:
                            </Htag>
                            <div className={styles.items_included_block} {...props}>
                                <div className={styles.items_included_block_item} {...props}><DoneIcon /><P>Встреча в день старта в Махачкале</P></div>
                                <div className={styles.items_included_block_item} {...props}><DoneIcon /><P>Трансфер на джипах</P></div>
                                <div className={styles.items_included_block_item} {...props}><DoneIcon /><P>Работа гида</P></div>
                                <div className={styles.items_included_block_item} {...props}><DoneIcon /><P>Трехразовое питание+перекусы в течение дня, чай/кофе и бонусы от гида;) (голодными Вы точно не останетесь, обещаем!)</P></div>
                                <div className={styles.items_included_block_item} {...props}><DoneIcon /><P>Проживание на протяжении всего тура</P></div>
                                <div className={styles.items_included_block_item} {...props}><DoneIcon /><P>Экскурсии</P></div>
                                <div className={styles.items_included_block_item} {...props}><DoneIcon /><P>Прогулка на катере</P></div>
                            </div> 
                        </div>
                        <div className={styles.items_canceled_block} {...props}>
                            <Htag tag='h2'>
                                В стоимость не включено
                            </Htag>
                            <div className={styles.items_included_block_cancel} {...props}>
                                <div className={styles.items_included_block_item} {...props}><CancelIcon /><P>Авиа/Жд билеты до Махачкалы и обратно </P></div>
                                <div className={styles.items_included_block_item} {...props}><CancelIcon /><P>Личные расходы (сувениры, личные покупки) </P></div>
                                <div className={styles.items_included_block_item} {...props}><CancelIcon /><P>Личные расходы (сувениры, личные покупки) </P></div>                                
                            </div> 

                        </div>

                        <div className={styles.aviasales_block} {...props}></div>


                        <div className={styles.travel_expert_block} {...props}>
                            <Htag tag='h2'>
                                Тревел-эксперт
                            </Htag>
                            <div className={styles.travel_expert_block_main} {...props}>

                            <div className={styles.card_expert_content_guide_name}>
                                <div className={styles.card_expert_content_guide_name_img}>

                                </div>
                                <div className={styles.card_expert_content_guide_name_about}>
                                    <Htag tag='h2'>
                                        Давид Исмаилов
                                    </Htag>
                                    <P>
                                        
                                        В путешествии главным экспертом и гидом для вас станет (данные скрыты) Магомед. С 2016 года Магомед провел сотни туров по всему Дагестану, 
                                        от юга до севера Республики. Природа, кухня, история - опыт гида позволяет открыть для Вас все стороны Дагестана, и показать Вам республику 
                                        "глазами местного"! скрыть

                                    </P>
                                </div>
                            </div>

                            <div className={styles.card_expert_content_guide_info_block}>
                                <div className={styles.card_expert_content}>
                                    <div className={styles.card_expert_content_place_info}>
                                        <Htag className={styles.card_expert_rating} tag='h4'>Рейтинг:</Htag>
                                        <Htag className={styles.card_expert_feedback} tag='h4'>Отзывы:</Htag>
                                        <Htag className={styles.card_expert_active_tours} tag='h4'>Активных туров:</Htag>
                                    </div>
                                    <div className={styles.card_expert_content_guide_info}>
                                        <Htag tag='h4' className={styles.card_expert_rating_num}><StarBigIcon /> 5.0</Htag>
                                        <Htag tag='h4' className={styles.card_expert_feedback_num}>211 отзывов</Htag>
                                        <Htag tag='h4' className={styles.card_expert_active_tours_num}>31 тур</Htag>
                                    </div>
                                </div>
                                <div className={styles.card_expert_content_guide_button}>
                                        Написать Давиду
                                </div>
                            </div>
                            
                            </div>

                        </div>


                </div> 
                    <div className={styles.wrapper_custom} {...props}>
                        <div className={styles.rout_travels_day_block_question} {...props}> 
                                <Htag tag='h2'>
                                    Вопросы по туру
                                </Htag>                           
                            <div className={styles.rout_travels_day_main_card_question} {...props}>
                                <div className={styles.rout_travels_day_main_card_info} {...props}>
                                    <div className={styles.rout_travels_day_main_card_info_header} {...props}>
                                        <Htag tag='h2'>
                                        А что будет если?
                                        </Htag>
                                        <ArrowUp />
                                    </div>
                                    <div className={styles.rout_travels_day_main_card_info_text_pink} {...props}>
                                        <P>
                                            Traveler.market — это маркетплейс авторских туров от тревел-экспертов и частных независимых гидов. 
                                            Авторские туры — это спонтанные и яркие возможности, предлагающие взять максимум от каждой точки маршрута. 
                                            Мы за непринужденный подход к групповым путешествиям, который больше похож на встречу со старыми друзьями.
                                        </P>
                                    </div>
                                </div>
                            </div>
                            <div className={styles.rout_travels_day_card} {...props}>
                                <div className={styles.rout_travels_day_main_card_info_header} {...props}>
                                    <Htag tag='h2'>
                                        Что взять с собой?
                                    </Htag>
                                    <ArrowDown />
                                </div>
                                <div className={styles.rout_travels_day_main_card_info_text} {...props}></div>
                            </div>
                            <div className={styles.rout_travels_day_card} {...props}>
                                <div className={styles.rout_travels_day_main_card_info_header} {...props}>
                                    <Htag tag='h2'>
                                        Какие ключевые особенносоти?
                                    </Htag>
                                    <ArrowDown />
                                </div>
                                <div className={styles.rout_travels_day_main_card_info_text} {...props}></div>
                            </div>
                            <div className={styles.rout_travels_day_card} {...props}>
                                <div className={styles.rout_travels_day_main_card_info_header} {...props}>
                                    <Htag tag='h2'>
                                        Что нового я увижу?
                                    </Htag>
                                    <ArrowDown />
                                </div>
                                <div className={styles.rout_travels_day_main_card_info_text} {...props}></div>
                            </div>
                           
                        </div>
                    </div>
            
            
        </div>
    );
};