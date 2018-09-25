import logging
import traceback
import uuid
from peewee import OperationalError
from database.model.topic_model import TopicModel

info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")


class TopicDAO(object):

    @staticmethod
    def update_topic(id, new_topic):
        try:
            update_query = (TopicModel.update({
                TopicModel.name: new_topic['name'] if 'name' in new_topic else TopicModel.name,
                TopicModel.matched_sentences: '\n'.join(new_topic[
                                                            'matched_sentences']) if 'matched_sentences' in new_topic else TopicModel.matched_sentences,
                TopicModel.prob: new_topic['prob'] if 'prob' in new_topic else TopicModel.prob,
                TopicModel.target: new_topic['target'] if 'target' in new_topic else TopicModel.target,
                TopicModel.matched_prob: new_topic[
                    'matched_prob'] if "matched_prob" in new_topic else TopicModel.matched_prob
            }).where(TopicModel.id == id))
            update_query.execute()
            updated_topic = (TopicModel.select().where(TopicModel.id == id)).execute()
            return {
                "id": updated_topic[0].id,
                "name": updated_topic[0].name,
                "matched_sentences": updated_topic[0].matched_sentences.split('\n'),
                "matched_prob": updated_topic[0].matched_prob,
                "target": updated_topic[0].target,
                "prob": updated_topic[0].prob
            }
        except Exception as e:
            error_logger.error("从数据库读取Topic时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def create_new_topic(name, matched_sentences, matched_prob, prob, target):
        try:
            id = str(uuid.uuid4())
            same_name_topics = (TopicModel.select().where(TopicModel.name == name)).execute()
            if len(list(same_name_topics)) != 0:
                return None
            else:
                TopicModel.create(
                    id=id,
                    matched_sentences='\n'.join(matched_sentences),
                    prob=float(prob),
                    target=target,
                    name=name,
                    matched_prob=matched_prob
                )
                new_topics = (TopicModel.select().where(TopicModel.id == id)).execute()
                return {
                    "id": new_topics[0].id,
                    "name": new_topics[0].name,
                    "matched_sentences": new_topics[0].matched_sentences.split('\n'),
                    "matched_prob": new_topics[0].matched_prob,
                    "target": new_topics[0].target,
                    "prob": new_topics[0].prob
                }
        except Exception as e:
            error_logger.error("从数据库读取Topic时发生其他错误, %s", traceback.format_exc(), extra={
                "host": 'localhost'})

    @staticmethod
    def view_topic_by_id(topic_id):
        try:
            topics = (TopicModel.select().where(TopicModel.id == topic_id)).execute()
            if len(list(topics)) == 1:
                return {
                    "id": topics[0].id,
                    "name": topics[0].name,
                    "matched_sentences": topics[0].matched_sentences.split('\n'),
                    "prob": topics[0].prob,
                    "target": topics[0].target,
                    "matched_prob": topics[0].matched_prob
                }
            else:
                return None
        except:
            error_logger.error("从数据库读取Topic时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def view_all_topics():
        try:
            topics = (TopicModel.select()).execute()
            packed_topics = []
            for topic in topics:
                packed_topics.append({
                    "id": topic.id,
                    "name": topic.name
                })
            return packed_topics
        except:
            error_logger.error("从数据库读取Topic时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def delete_topic(topic_id):
        try:
            delete_query = TopicModel.delete().where(TopicModel.id == topic_id)
            affected_rows = delete_query.execute()
            return affected_rows
        except Exception as e:
            error_logger.error("从数据库读取Topic时发生其他错误, %s", traceback.format_exc(), extra={
                "host": 'localhost'})
