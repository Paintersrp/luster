import { FC, useEffect, useState } from 'react';

import { ButtonBar } from '@/components/Built';
import { Container, Flexer, Item } from '@/components/Containers';
import { Base, Divider, Text } from '@/components/Elements';
import { FormGenerator } from '@/components/Form';
import { Media } from '@/components/Media';
import { palettes } from '@/utils';

import { ServiceType } from '../../types';

type ServiceAboutProps = {
  data: ServiceType;
  editMode: boolean;
};

export const ServiceAbout: FC<ServiceAboutProps> = ({ data, editMode }) => {
  const [aboutData, setAboutData] = useState(data);
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    setAboutData(data);
  }, [data]);

  const updateService = (updateService: ServiceType) => {
    setAboutData(updateService);
    setEditing(false);
  };

  return (
    <Base>
      {!editing && editMode && (
        <ButtonBar
          justifyContent="flex-end"
          editClick={() => setEditing(!editing)}
          adminLink="servicetier"
          text="Service"
          obj={aboutData.id}
          mb={8}
        />
      )}
      {!editing ? (
        <Container j="fs" a="fs" mb={24}>
          <Item xs={12} sm={12} md={12} lg={6} fd="column">
            <Text t="h5" a="c" c={palettes.primary.main}>
              About Our {aboutData.service_title} Service
            </Text>
            <Divider mt={8} mb={8} />
            <Text t="body1" mb={8}>
              {aboutData.paragraph_one}
            </Text>
            <Text t="body1" mb={8}>
              {aboutData.paragraph_two}
            </Text>
            <Text t="body1" mb={16}>
              {aboutData.paragraph_three}
            </Text>
          </Item>
          <Item xs={12} sm={12} md={12} lg={6} align="flex-start" pl={12}>
            <div style={{ minWidth: '100%', maxHeight: 300 }}>
              <Media src={aboutData.image} altText={aboutData.service_title} />
            </div>
          </Item>
        </Container>
      ) : (
        <Flexer j="c" mb={24}>
          <FormGenerator
            title="Edit Service Header Item"
            endpoint={`servicetier/${data.id}/`}
            data={data}
            onUpdate={updateService}
            handleCancel={() => setEditing(!editing)}
            width="50%"
            excludeKeys={['id', 'image', 'features', 'supported_sites', 'price', 'service_title']}
            multilineKeys={['paragraph_one', 'paragraph_two', 'paragraph_three']}
            px={3}
            py={3}
            br={8}
            placement="bottom"
            imageMixin
            boxShadow
          />
        </Flexer>
      )}
    </Base>
  );
};
