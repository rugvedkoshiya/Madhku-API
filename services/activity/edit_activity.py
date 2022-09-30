from datetime import datetime
from models.conn import Session
from services.json_response import JsonResponse
from services.validators.common_checker import activityDistanceChecker, activityTitleChecker, activityTypeChecker, datetimeChecker
from flask_jwt_extended.utils import get_jwt_identity
from dataclasses import asdict
from models.activity import Activity
from sqlalchemy.sql.expression import and_

def editActivity(reqObj, activityId):
    response = JsonResponse()
    session = Session()
    userId = get_jwt_identity()

    try:
        data = {}
        activityDistance = None
        activityType = None
        startAtDatetime = None
        endAtDatetime = None

        activityTitle = activityTitleChecker(response, reqObj.get("title"))

        if activityTitle != None:
            activityDistance = activityDistanceChecker(response, reqObj.get("distance"))
        
        if activityDistance != None:
            activityType = activityTypeChecker(response, reqObj.get("activity_type"))

        if activityType != None:
            startAtDatetime = datetimeChecker(response, reqObj.get("start_at"))
            
        if startAtDatetime != None:
            endAtDatetime = datetimeChecker(response, reqObj.get("end_at"))
    

        if endAtDatetime != None:
            activityObj = (
                session.query(
                    Activity
                )
                .filter(
                    and_(
                        Activity.user_id == userId,
                        Activity.activity_id == activityId,
                    )
                )
                .first()
            )
            if activityObj:
                activityObj.title = activityTitle
                activityObj.distance = activityDistance
                activityObj.activity_type = activityType
                activityObj.note = reqObj.get("note")
                activityObj.start_at = startAtDatetime
                activityObj.end_at = endAtDatetime
                activityObj.modified_at = datetime.utcnow()

                session.add(activityObj)
                session.flush()
                data = asdict(activityObj)
                response.setStatus(200)
                response.setMessage("Activity edited successfully !!")

        response.setData(data)
        session.commit()

    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Internal Server Error in Edit Activity => " + str(e))

    finally:
        session.close()
        return response.returnResponse()