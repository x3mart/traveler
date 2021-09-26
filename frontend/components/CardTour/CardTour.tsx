import styles from './CardTour.module.css';
import { CardTourProps } from './CardTour.props';
import cn from 'classnames';
import { Tag, Htag } from '../../components/';
import StarIcon from '/public/Star.svg';
import LikeIcon from '/public/Like.svg';
    


export const CardTour = ({ block_style, children, className, ...props }: CardTourProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.card_tour, className, {
                [styles.card_tour]: block_style == 'card_tour',
            })}
            {...props}
            
        >    
                  
            {children}
            <Tag size='b'>
                <div className={styles.card_tour_image}>
                    <LikeIcon />
                </div>
                <div className={styles.card_tour_content}>
                    <div className={styles.card_tour_content_place_info}>
                        <Htag tag='h4'>Вьетнам</Htag>
                        <Htag tag='h3'>Неизведанные места и тропы</Htag>
                    </div>
                    <div className={styles.card_tour_content_guide_info}>
                        <div className={styles.card_tour_content_guide_info_name}>
                            <div className={styles.card_tour_content_guide_info_name_avatar}>

                            </div>
                            <div className={styles.card_tour_content_guide_info_name_raiting}>
                                <Htag tag='h4'>Мария</Htag>
                                <Htag tag='h4'>
                                    <StarIcon />
                                    <span className={styles.raiting_star}>4.9</span>
                                    (132)  
                                </Htag>
                            </div>
                        </div>
                        <div className={styles.card_tour_content_guide_info_cost}>
                            <Htag tag='h4'>7 дн. (21 - 28 мар)</Htag> 
                            <Htag tag='h3'>от 80.000 {'\u20bd'}</Htag>
                        </div>
                    </div>
                </div>
            </Tag>     
             
        </div>
    );
};