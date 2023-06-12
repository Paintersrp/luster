import { FC, Fragment, useEffect, useState } from 'react';

import { ButtonBar, ManyToManyEdit } from '@/components/Built';
import { Flexer } from '@/components/Containers';
import { BaseProps, List, Text } from '@/components/Elements';
import { IconTextItem } from '@/components/Media';
import { palettes } from '@/utils';

import { JobType } from '../types';

interface JobQualificationProps {
  title: string;
  data: any;
  editMode: boolean;
  updateData: (updatedData: any) => void;
  fieldName: 'requirements' | 'responsibilities';
  id: number;
}

export const JobQualification: FC<JobQualificationProps> = ({
  title,
  data,
  editMode,
  updateData,
  fieldName,
  id,
}) => {
  const [edit, setEdit] = useState(false);

  const handleUpdateData = (updatedData: any) => {
    updateData(updatedData);
    setEdit(false);
  };

  return (
    <Fragment>
      {!edit && (
        <List px={0} spacing={0} boxShadow={0} dividers={false} className="fade-in">
          <Text t="h3" mt={16} mb={6}>
            {title}
          </Text>
          {data &&
            data[fieldName].map((item: any, index: number) => (
              <IconTextItem
                key={index}
                icon="check_circle"
                text={item.detail}
                iconColor={index % 2 === 0 ? palettes.primary.main : palettes.secondary.main}
                iconSize="21px"
              />
            ))}
        </List>
      )}
      {!edit && editMode && <ButtonBar editClick={() => setEdit(true)} text={title} mt={8} />}
      {edit && (
        <ManyToManyEdit
          data={data}
          updateData={handleUpdateData}
          endpoint="jobposting"
          handleCancel={() => setEdit(!edit)}
          id={id}
          fieldName={fieldName}
          title={`Edit ${title}`}
        />
      )}
    </Fragment>
  );
};

interface JobQualificationsProps extends BaseProps {
  job: JobType;
  editMode: boolean;
}

export const JobQualifications: FC<JobQualificationsProps> = ({ job, editMode, ...rest }) => {
  const [jobData, setJobData] = useState(job);

  useEffect(() => {
    setJobData(job);
  }, [job]);

  const updateData = (updatedData: any) => {
    setJobData(updatedData);
  };

  return (
    <Flexer fd="column" {...rest}>
      <JobQualification
        title="Job Requirements"
        data={jobData}
        editMode={editMode}
        updateData={updateData}
        fieldName="requirements"
        id={jobData.id}
      />
      <JobQualification
        title="Job Responsibilities"
        data={jobData}
        editMode={editMode}
        updateData={updateData}
        fieldName="responsibilities"
        id={jobData.id}
      />
    </Flexer>
  );
};
