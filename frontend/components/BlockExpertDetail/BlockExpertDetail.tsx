import styles from './BlockExpertDetail.module.css';
import { BlockExpertDetailProps } from './BlockExpertDetail.props';
import cn from 'classnames';
import { Htag, P } from '../../components/';
import ClockIcon from '../../public/clock_big.svg';
import ChatIcon from '../../public/chat.svg';
import DocIcon from '../../public/doc.svg';
import TelIcon from '../../public/tel.svg';
import MailIcon from '../../public/mail.svg';


export const BlockExpertDetail = ({ block_style, children, className, ...props }: BlockExpertDetailProps): JSX.Element => {     
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                <div className={styles.expert_detail_block} {...props}>
                    <div className={styles.expert_detail_block_photo} {...props}>
                        <div className={styles.expert_detail_block_photo_face} {...props}></div>
                        <div className={styles.expert_detail_block_photo_reg} {...props}>
                            Зарегистрирован 16 марта 2015г.
                        </div>
                    </div>
                    <div className={styles.expert_detail_block_content} {...props}>
                        <div className={styles.expert_detail_block_content_last_visit} {...props}>
                            Был(а) на сайте вчера в 22:06
                        </div>
                        <div className={styles.expert_detail_block_content_last_visit} {...props}>
                            <Htag tag="h2">Здравствуйте, меня зовут Давид</Htag>
                            <P>Эй! Ты готов к приключениям !!?? <br />
                                Да-Да! Именно ПРИКЛЮЧЕНИЯМ!<br />
                                С 2014 года наша команда выросла до 15 человек, а проект вырос до реальной компании-организатора приключений в стиле 
                                DiscoveryКаждое наше путешествие – взрывная смесь культуры страны, адреналина, сёрфинга и драйва. Подойдут тем, кто ищет 
                                не просто Авторский тур, а ПРИКЛЮЧЕНИЕ, которое будете прокручивать в голове как минимум до следующей поездки с нами!
                                Все наши маршруты прошли неоднократную проверку, почитайте отзывы или задайте вопрос по любой мелочи :)
                            </P>
                            <P>
                                Если ты такой же фанат новых впечатлений и криков "ВАУ!! Охренеть, вот это ...."– то просто выбирай страну, где ещё не 
                                был и поехали вместе!
                            </P> <br />
                            <span>развернуть</span>
                        </div>
                    </div>
                    <div className={styles.expert_detail_block_contacts} {...props}>
                        <div className={styles.expert_detail_block_contacts_button} {...props}>
                            Написать в чат
                        </div>
                        <div className={styles.expert_detail_block_contacts_info} {...props}>
                            <div className={styles.expert_detail_block_contacts_info_detail} {...props}>
                                <ClockIcon />
                                <p>Среднее время ответа:</p>
                                <span>2ч.</span>
                            </div>
                            <div className={styles.expert_detail_block_contacts_info_detail} {...props}>
                                <ChatIcon />
                                <p>Отзывов туристов:</p>
                                <span>210</span>
                            </div>
                            <div className={styles.expert_detail_block_contacts_info_detail_text} {...props}>
                                Давид подтвердил:
                            </div>
                            <div className={styles.expert_detail_block_contacts_info_detail} {...props}>
                                <DocIcon />
                                <p>Документы</p>
                            </div>
                            <div className={styles.expert_detail_block_contacts_info_detail} {...props}>
                                <TelIcon />
                                <p>Номер телефона</p>
                            </div>
                            <div className={styles.expert_detail_block_contacts_info_detail} {...props}>
                                <MailIcon />
                                <p>Личный e-mail</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div> 
            
        </div>
    );
};