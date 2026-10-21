from typing import Annotated
from uuid import UUID

from app.application.schemas.project import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
    ProjectWithChatsRead,
)
from app.application.services.projects.commands.create_project import (
    CreateProjectService,
)
from app.application.services.projects.commands.delete_project import (
    DeleteProjectService,
)
from app.application.services.projects.commands.update_project import (
    UpdateProjectService,
)
from app.application.services.projects.queries.get_all_project import (
    GetAllProjectService,
)
from app.application.services.projects.queries.get_project import GetProjectService
from app.domain.exceptions.project import ProjectNotFoundError
from app.infrastructure.dependencies.entities.projects.command.create_project import (
    create_project_service,
)
from app.infrastructure.dependencies.entities.projects.command.delete_project import (
    delete_project_service,
)
from app.infrastructure.dependencies.entities.projects.command.update_project import (
    update_project_service,
)
from app.infrastructure.dependencies.entities.projects.queries.get_all_project import (
    get_all_project_service,
)
from app.infrastructure.dependencies.entities.projects.queries.get_project import (
    get_project_service,
)
from app.presentation.api.exceptions.project import ProjectNotFoundHTTPException
from app.presentation.api.schemas.responses import SuccessResponse
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get(
    "/",
    response_model=SuccessResponse[list[ProjectRead]],
    status_code=status.HTTP_200_OK,
)
async def get_projects(
    projects_service: Annotated[GetAllProjectService, Depends(get_all_project_service)],
):
    data = await projects_service()
    return SuccessResponse(data=data)


@router.get(
    "/{project_id}",
    response_model=SuccessResponse[ProjectWithChatsRead],
    status_code=status.HTTP_200_OK,
)
async def get_project(
    project_id: UUID,
    project_service: Annotated[GetProjectService, Depends(get_project_service)],
):
    try:
        data = await project_service(project_id)
        return SuccessResponse(data=data)
    except ProjectNotFoundError as e:
        raise ProjectNotFoundHTTPException(str(e))


@router.post(
    "/",
    response_model=SuccessResponse[dict[str, UUID]],
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project_data: ProjectCreate,
    project_service: Annotated[CreateProjectService, Depends(create_project_service)],
):
    data = await project_service(project_data)
    return SuccessResponse(data=data)


@router.patch(
    "/{project_id}",
    response_model=SuccessResponse[dict[str, UUID]],
    status_code=status.HTTP_200_OK,
)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    project_service: Annotated[UpdateProjectService, Depends(update_project_service)],
):
    try:
        data = await project_service(project_id, project_data)
        return SuccessResponse(data=data)
    except ProjectNotFoundError as e:
        raise ProjectNotFoundHTTPException(str(e))


@router.delete(
    "/{project_id}",
    response_model=SuccessResponse[dict[str, UUID]],
    status_code=status.HTTP_200_OK,
)
async def delete_project(
    project_id: UUID,
    project_service: Annotated[DeleteProjectService, Depends(delete_project_service)],
):
    try:
        data = await project_service(project_id)
        return SuccessResponse(data=data)
    except ProjectNotFoundError as e:
        raise ProjectNotFoundHTTPException(str(e))
