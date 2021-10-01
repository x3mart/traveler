import styles from './CardTourLarge.module.css';
import { CardTourLargeProps } from './CardTourLarge.props';
import cn from 'classnames';
import { Tag, Htag } from '..';
import StarIcon from '/public/Star.svg';
import LikeIcon from '/public/Like.svg';
    


export const CardTourLarge = ({ block_style, children, className, ...props }: CardTourLargeProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.card_tour, className, {
                [styles.card_tour]: block_style == 'card_tour',
            })}
            {...props}
            
        >    
                  
            {children}
            <Tag size='l'>
                <div className={styles.card_tour_image}>
                    <LikeIcon />
                </div>
                <div className={styles.card_tour_content}>
                    <div className={styles.card_tour_content_place_info}>
                        <Htag tag='h4'>Армения</Htag>
                        <Htag tag='h3'>По горам на велосипеде</Htag>
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
                            <Htag tag='h3'>от 80.000 <span>{'\u20bd'}</span></Htag>
                        </div>
                    </div>
                </div>
            </Tag>     
             
        </div>
    );
};